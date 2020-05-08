from django import forms
from django.core.exceptions import ValidationError
from Bio.Alphabet.IUPAC import IUPACProtein
from .models import PesticidalProteinDatabase, Description
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, HTML, ButtonHolder
from crispy_forms.bootstrap import AppendedText

ALLOWED_AMINOACIDS = set(IUPACProtein.letters)
# ALLOWED_NUCLEOTIDE = set(IUPACAmbiguousDNA.letters)

# maximum number of query sequences in form
NEEDLE_MAX_NUMBER_SEQ_IN_INPUT = 1

# Error messages
NEEDLE_CORRECT_SEQ_ERROR_MSG = "please paste correct sequence!"
NEEDLE_CORRECT_SEQ_TOO_SHORT_ERROR_MSG = "Too short sequence!"
NEEDLE_SEQUENCE_TYPE = "Currently, protein sequence is allowed"
NEEDLE_CORRECT_SEQ_MAX_SEQ_NUMB_ERROR_MSG = "Too many sequences, maximum is {}".format(
    NEEDLE_MAX_NUMBER_SEQ_IN_INPUT)


def validate_sequence(sequence: str, sequence_is_protein=True):
    """ Validate protein sequence """
    tmp_seq = tempfile.NamedTemporaryFile(mode="wb+", delete=False)

    if len(str(sequence.strip())) == 0:
        raise forms.ValidationError(NEEDLE_CORRECT_SEQ_ERROR_MSG)

    if str(sequence).strip()[0] != ">":
        tmp_seq.write(">seq1\n".encode())

    tmp_seq.write(sequence.encode())
    tmp_seq.close()

    records = SeqIO.index(tmp_seq.name, "fasta")
    record_count = len(records)

    if record_count == 0:
        raise forms.ValidationError(NEEDLE_CORRECT_SEQ_ERROR_MSG)

    if record_count > NEEDLE_MAX_NUMBER_SEQ_IN_INPUT:
        raise forms.ValidationError(NEEDLE_CORRECT_SEQ_MAX_SEQ_NUMB_ERROR_MSG)

    # read sequence from the written temporary file
    sequence_in_file = SeqIO.parse(tmp_seq.name, "fasta")
    # print(sequence_in_file.seq)
    sequence = None
    for record in sequence_in_file:

        sequence = record.seq

    if sequence_is_protein:
        check_allowed_letters(str(sequence), ALLOWED_AMINOACIDS)
    else:
        return NEEDLE_SEQUENCE_TYPE

    return tmp_seq.name


def check_allowed_letters(seq, allowed_letter_as_set):
    """ Validate sequence: Rise an error if sequence contains undesirable letter."""

    # set of unique letters in sequence
    seq_set = set(seq)

    not_allowed_letters_in_seq = [x for x in seq_set if str(
        x).upper() not in allowed_letter_as_set]

    if len(not_allowed_letters_in_seq) > 0:
        raise forms.ValidationError(
            "This sequence type cannot contain letters: " +
            ", ".join(not_allowed_letters_in_seq)
        )


def check_protein_nucleotide(seq):
    sequence_is_protein = check_allowed_letters(
        str(sequence), ALLOWED_AMINOACIDS)
    return sequence_is_protein


class SearchForm(forms.Form):
    # search_term = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False,
    #
    # choices=SEARCH_CHOICES)
    SEARCH_CHOICES = (
        ('full name', 'FULL NAME'),
        ('category', 'CATEGORY'),
        ('oldname', 'OLDNAME'),
        ('accession', 'ACCESSION'),
        ('year', 'YEAR'),
    )

    search_term = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Search'}))
    search_fields = forms.ChoiceField(choices=SEARCH_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search_term'].error_messages = {
            'required': 'Please type a protein name'}
        self.fields['search_term'].label = ''
        self.fields['search_fields'].label = ''
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('search_term',
                       css_class='form-group col-md-10'),
            ),
            Row(
                Column('search_fields',
                       css_class='form-group col-md-10'),
            ))

    def clean_search_term(self):
        data = self.cleaned_data['search_term']

        if data is None:
            raise ValidationError(
                "Please provide the keywords to search in the database")

        return data


class UserSubmittedSequenceAnalysis(forms.ModelForm):

    sequences_in_form = forms.CharField(
        widget=forms.Textarea, required=False, label="protein sequence")

    def clean_sequences_in_form(self):
        sequences_in_form = self.cleaned_data['sequences_in_form']
        if sequences_in_form:
            return validate_sequence(sequences_in_form, sequence_is_protein=True)
        return sequences_in_form

    class Meta:
        model = PesticidalProteinDatabase
        fields = ['name', 'sequence']


class DownloadForm(forms.Form):

    category_type = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices='',
        label='',
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(DownloadForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'id-download'
        self.helper.form_class = 'downloadforms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'category_download'

        self.helper.add_input(Submit('submit', 'Download'))

        categories = PesticidalProteinDatabase.objects.order_by(
            'name').values_list('name', flat=True)
        description = Description.objects.order_by(
            'name')

        self.category_prefixes = {}
        self.category_description = {}
        self.category_options = [('all', 'ALL')]
        for category in categories:
            prefix = category[0:3]
            self.category_prefixes[prefix.lower()] = prefix.upper()

        # for detail in description:
        #     for option in self.category_options:
        #         if detail.name.lower() == max(option):
        #             print(option)
        for key, value in self.category_prefixes.items():
            for detail in description:
                if detail.name.lower() == key.lower():
                    self.category_description[key.lower(
                    )] = value + "      :  " + detail.description

        self.category_options.extend(
            sorted(self.category_description.items(), key=lambda x: x[0][:3]))
        self.fields['category_type'].choices = self.category_options
        self.fields['category_type'].label = ''

    def clean_category_type(self):
        category_type = self.cleaned_data['category_type']

    # def save(self):
    #     context = {
    #         'proteins': PesticidalProteinDatabase.objects.all()
    #     }
    #
    #     file = StringIO()
    #     data = list(context.get('proteins'))
    #
    #     for item in data:
    #         if item.name[:3].lower() in str(category_type):
    #             fasta = textwrap.fill(item.sequence, 80)
    #             str_to_write = f">{item.name}\n{fasta}\n"
    #             file.write(str_to_write)
    #
    #     if 'all' in category_type:
    #         for item in data:
    #             fasta = textwrap.fill(item.sequence, 80)
    #             str_to_write = f">{item.name}\n{fasta}\n"
    #             file.write(str_to_write)
    #
    #     download_file = f"{'_'.join(category_type)}_fasta_sequences.txt"
    #     return download_file

from django import forms
from django.core.exceptions import ValidationError
from Bio.Alphabet.IUPAC import IUPACProtein
from .models import PesticidalProteinDatabase, FeedbackData

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
        ('name_category', 'NAME_CATEGORY'),
        ('oldname', 'OLDNAME'),
        ('accession', 'ACCESSION'),
        ('year', 'YEAR'),
    )

    search_term = forms.CharField(required=True)
    search_fields = forms.ChoiceField(choices=SEARCH_CHOICES, required=False, )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search_term'].error_messages = {
            'required': 'Please type a protein name'}

    def clean_search_term(self):
        data = self.cleaned_data['search_term']
        print(data)

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


class FeedbackDataForm(forms.ModelForm):

    class Meta:
        model = FeedbackData
        fields = ['from_email', 'subject', 'message']


# class TaxoForm(forms.Form):
#     OPTIONS = (
#         ('n-terminal domain', 'N-TERMINAL DOMAIN'),
#         ('c-terminal domain', 'C-TERMINAL DOMAIN'),
#         ('m-terminal domain', 'M-TERMINAL DOMAIN'),
#         ('full length', 'FULL LENGTH'),
#     )
    # domain_type = forms.CharField(widget=forms.Select(choices=OPTIONS))
    # domain_type = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=OPTIONS)
    #
    # Bacillus cereus - 1396
    # Bacillus subtilis - 1423

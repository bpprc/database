from crispy_forms.bootstrap import AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    HTML,
    ButtonHolder,
    Column,
    Layout,
    Row,
    Submit,
)
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator

from .models import Description, PesticidalProteinDatabase

RECAPTCHA_PUBLIC_KEY = "6Lc-HfMUAAAAALHi0-vkno4ntkJvLW3rAF-d5UXT"

ALLOWED_AMINOACIDS = {
    "E",
    "Q",
    "L",
    "Y",
    "V",
    "W",
    "I",
    "A",
    "H",
    "G",
    "P",
    "S",
    "R",
    "C",
    "T",
    "F",
    "K",
    "N",
    "D",
    "M",
}
# ALLOWED_NUCLEOTIDE = set(IUPACAmbiguousDNA.letters)

# maximum number of query sequences in form
NEEDLE_MAX_NUMBER_SEQ_IN_INPUT = 1

# Error messages
NEEDLE_CORRECT_SEQ_ERROR_MSG = "please paste correct sequence!"
NEEDLE_CORRECT_SEQ_TOO_SHORT_ERROR_MSG = "Too short sequence!"
NEEDLE_SEQUENCE_TYPE = "Currently, protein sequence is allowed"
NEEDLE_CORRECT_SEQ_MAX_SEQ_NUMB_ERROR_MSG = (
    "Too many sequences, maximum is {}".format(
        NEEDLE_MAX_NUMBER_SEQ_IN_INPUT
    )
)


def validate_sequence(sequence: str, sequence_is_protein=True):
    """Validate protein sequence"""
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
        raise forms.ValidationError(
            NEEDLE_CORRECT_SEQ_MAX_SEQ_NUMB_ERROR_MSG
        )

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
    """Validate sequence: Rise an error if sequence contains undesirable letter."""

    # set of unique letters in sequence
    seq_set = set(seq)

    not_allowed_letters_in_seq = [
        x
        for x in seq_set
        if str(x).upper() not in allowed_letter_as_set
    ]

    if len(not_allowed_letters_in_seq) > 0:
        raise forms.ValidationError(
            "This sequence type cannot contain letters: "
            + ", ".join(not_allowed_letters_in_seq)
        )


def check_protein_nucleotide(seq):
    sequence_is_protein = check_allowed_letters(
        str(sequence), ALLOWED_AMINOACIDS
    )
    return sequence_is_protein


class SearchForm(forms.Form):

    SEARCH_CHOICES = (
        ("name", "Name"),
        ("old name/other name", "Old Name/Other Name"),
        ("accession", "Accession"),
        ("holotype", "Holotype"),
        ("structure", "Structure"),
    )

    search_term = forms.CharField(
        label="",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Search"}),
    )
    search_fields = forms.ChoiceField(
        choices=SEARCH_CHOICES, required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["search_term"].error_messages = {
            "required": "Please type a protein name"
        }
        self.fields["search_term"].label = ""

        validators = [
            v
            for v in self.fields["search_term"].validators
            if not isinstance(v, MinLengthValidator)
        ]
        min_length = 3
        validators.append(MinLengthValidator(min_length))
        # print(validators)
        self.fields["search_term"].validators = validators

        # self.fields['search_term'].min_length = 3
        self.fields["search_fields"].label = ""
        self.helper = FormHelper()
        self.helper.form_id = "id-SearchForm"
        self.helper.form_class = "SearchForm"
        self.helper.form_method = "post"
        self.helper.form_action = "search_database"
        self.helper.add_input(Submit("submit", "Submit"))
        self.helper.layout = Layout(
            Row(
                Column(
                    "search_term",
                    css_class="form-group input-group-append col-md-6",
                ),
                css_class="form-row",
            ),
            Row(
                Column(
                    "search_fields", css_class="form-group col-md-6"
                ),
                css_class="form-row",
            ),
        )

    def clean_search_term(self):
        data = self.cleaned_data["search_term"]

        if data is None:
            raise ValidationError(
                "Please provide the keywords to search in the database"
            )
        elif data != "R1" and len(data) < 3:
            raise ValidationError(
                "Please keep the search term under 3 characters"
            )

        return data


class UserSubmittedSequenceAnalysis(forms.ModelForm):

    sequences_in_form = forms.CharField(
        widget=forms.Textarea, required=False, label="protein sequence"
    )

    def clean_sequences_in_form(self):
        sequences_in_form = self.cleaned_data["sequences_in_form"]
        if sequences_in_form:
            return validate_sequence(
                sequences_in_form, sequence_is_protein=True
            )
        return sequences_in_form

    class Meta:
        model = PesticidalProteinDatabase
        fields = ["name", "sequence"]


class DownloadForm(forms.Form):

    category = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices="",
        label="",
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(DownloadForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = "category"
        self.helper.form_class = "categoryform"
        self.helper.form_method = "post"
        self.helper.form_action = "category_download"

        self.helper.add_input(Submit("submit", "Download"))

        categories = PesticidalProteinDatabase.objects.order_by(
            "name"
        ).values_list("name", flat=True)
        description = Description.objects.order_by("name")

        self.category_prefixes = {}
        self.category_description = {}
        self.category_options = [("all", "All")]
        for category in categories:
            prefix = category[0:3]
            self.category_prefixes[prefix.lower()] = prefix.title()

        for key, value in self.category_prefixes.items():
            for detail in description:
                if detail.name.lower() == key.lower():
                    self.category_description[key.lower()] = (
                        value + "      :  " + detail.description
                    )

        self.category_options.extend(
            sorted(
                self.category_description.items(),
                key=lambda x: x[0][:3],
            )
        )
        self.fields["category"].choices = self.category_options
        # self.fields['category_type'].label = ''
        # self.helper.layout = Layout(
        #     'category_type',
        #     HTML('<div class="form-group"><div class="g-recaptcha" data-sitekey="%s"></div></div>' %
        #          RECAPTCHA_PUBLIC_KEY),
        # )

    def clean_category_type(self):
        category_type = self.cleaned_data["category"]

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


class HolotypeForm(forms.Form):
    holotype = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices="",
        label="",
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(HolotypeForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = "holotype"
        self.helper.form_class = "holotypeform"
        self.helper.form_method = "post"
        self.helper.form_action = "holotype_download"

        self.helper.add_input(Submit("submit", "Download"))

        self.category_options = [("holotype", "holotype")]

        self.fields["holotype"].choices = self.category_options
        self.fields["holotype"].label = ""


class ThreedomainDownloadForm(forms.Form):

    threedomain = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices="",
        label="",
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(ThreedomainDownloadForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = "threedomain"
        self.helper.form_class = "threedomaindownloadform"
        self.helper.form_method = "post"
        self.helper.form_action = "threedomain_download"

        self.helper.add_input(Submit("submit", "Download"))

        # categories = PesticidalProteinDatabase.objects.order_by(
        #     'name').values_list('name', flat=True)
        # description = Description.objects.order_by(
        #     'name')

        # self.category_prefixes = {}
        # self.category_description = {}
        self.category_options = [
            ("full_length", "Full_Length"),
            ("domain1", "Domain1"),
            ("domain2", "Domain2"),
            ("domain3", "Domain3"),
        ]
        # for category in categories:
        #     prefix = category[0:3]
        #     self.category_prefixes[prefix.lower()] = prefix.title()
        #
        # for key, value in self.category_prefixes.items():
        #     for detail in description:
        #         if detail.name.lower() == key.lower():
        #             self.category_description[key.lower(
        #             )] = value + "      :  " + detail.description
        #
        # self.category_options.extend(
        #     sorted(self.category_description.items(), key=lambda x: x[0][:3]))
        self.fields["threedomain"].choices = self.category_options
        # self.fields['threedomain_type'].label = ''
        # self.helper.layout = Layout(
        #     'category_type',
        #     HTML('<div class="form-group"><div class="g-recaptcha" data-sitekey="%s"></div></div>' %
        #          RECAPTCHA_PUBLIC_KEY),
        # )

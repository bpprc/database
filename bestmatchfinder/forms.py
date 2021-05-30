import tempfile

from Bio import Seq, SeqIO
from crispy_forms.helper import FormHelper
from django import forms

from database.models import PesticidalProteinDatabase

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
NEEDLE_CORRECT_SEQ_MAX_SEQ_NUMB_ERROR_MSG = "Too many sequences, maximum is {}".format(NEEDLE_MAX_NUMBER_SEQ_IN_INPUT)


def write_sequence_file(sequence: str):
    """Validate protein sequence"""

    # open a temperorary file
    tmp_seq = tempfile.NamedTemporaryFile(mode="wb+", delete=False)

    # if sequence is none raise the ValidationError
    if len(str(sequence.strip())) == 0:
        raise forms.ValidationError(NEEDLE_CORRECT_SEQ_ERROR_MSG)

    # Write fasta sequence
    if str(sequence).strip()[0] != ">":
        tmp_seq.write(">seq1\n".encode())

    tmp_seq.write(sequence.encode())
    tmp_seq.close()
    # Return name of the temporary file
    return tmp_seq.name


def guess_if_protein(seq, thresh=0.99):
    """Guess if the given sequence is Protein."""
    # protein_letters = ['C', 'D', 'S', 'Q', 'K','I','P','T','F','N','G',
    #                'H','L','R','W','A','V','E','Y','M']
    dna_letters = ["A", "C", "G", "T"]

    for record in SeqIO.parse(seq, "fasta"):
        seq = record.seq

    seq = seq.upper()
    protein_alpha_count = 0
    for letter in dna_letters:
        protein_alpha_count += seq.count(letter)

    return len(seq) == 0 or float(protein_alpha_count) / float(len(seq)) >= thresh


class SequenceForm(forms.Form):
    sequence_in_form = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["sequence_in_form"].label = ""

    def clean_sequence_in_form(self):
        sequence_in_form = self.cleaned_data["sequence_in_form"]

        if sequence_in_form:
            return write_sequence_file(sequence_in_form)
        return sequence_in_form

    def clean(self):
        sequence_in_form = self.cleaned_data["sequence_in_form"]

        if sequence_in_form:
            sequence_is_protein = guess_if_protein(sequence_in_form)

        if not sequence_in_form:
            raise forms.ValidationError("Please paste valid protein sequences")

        if sequence_is_protein:
            raise forms.ValidationError("Currently, it supports only protein sequences")

        return self.cleaned_data


class SearchDatabaseForm(forms.Form):

    protein_id1 = forms.ModelChoiceField(
        queryset=PesticidalProteinDatabase.objects.all(),
        required=False,
        label="Database protein 1",
    )
    sequence1_in_form = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label="Or user-supplied sequence 1 (plain or fasta format)",
    )
    protein_id2 = forms.ModelChoiceField(
        queryset=PesticidalProteinDatabase.objects.all(),
        required=False,
        label="Database protein 2",
    )
    sequence2_in_form = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label="Or user-supplied sequence 2 (plain or fasta format)",
    )
    tool = forms.ChoiceField(
        required=False,
        choices=[("needle", "Needle"), ("blastp", "BLASTP")],
    )

    def clean_sequence1_in_form(self):

        sequence1_in_form = self.cleaned_data["sequence1_in_form"]

        if sequence1_in_form:
            return write_sequence_file(sequence1_in_form)

        return sequence1_in_form

    def clean_sequence2_in_form(self):

        sequence2_in_form = self.cleaned_data["sequence2_in_form"]

        if sequence2_in_form:
            return write_sequence_file(sequence2_in_form)

        return sequence2_in_form

    def clean(self):
        protein1 = self.cleaned_data["protein_id1"]
        protein2 = self.cleaned_data["protein_id2"]
        sequence1_in_form = self.cleaned_data["sequence1_in_form"]
        sequence2_in_form = self.cleaned_data["sequence2_in_form"]

        if sequence1_in_form:
            sequence_is_protein = guess_if_protein(sequence1_in_form)
            if sequence_is_protein:
                raise forms.ValidationError("Currently, it supports only protein sequences")

        if sequence2_in_form:
            sequence_is_protein = guess_if_protein(sequence2_in_form)
            if sequence_is_protein:
                raise forms.ValidationError("Currently, it supports only protein sequences")

        if protein1 and sequence1_in_form:
            raise forms.ValidationError("Please select only one of Sequence / Choice")
        elif not protein1 and not sequence1_in_form:
            raise forms.ValidationError("Please select only one of Sequence / Choice")

        if protein2 and sequence2_in_form:
            raise forms.ValidationError("Please select only one of Sequence / Choice")
        elif not protein2 and not sequence2_in_form:
            raise forms.ValidationError("Please select only one of Sequence / Choice")

        # if not sequence_is_protein1 and not sequence_is_protein2:
        #     raise forms.ValidationError("Currently, it supports only protien sequences")

        return self.cleaned_data

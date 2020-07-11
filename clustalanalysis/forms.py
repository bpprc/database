import tempfile
import textwrap
import subprocess
import ast
from Bio.Align.Applications import ClustalOmegaCommandline
from database.models import PesticidalProteinDatabase, UserUploadData, ProteinDetail
from django import forms
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from Bio import SeqIO
from Bio import Seq
from django.forms import widgets
from django.db.models import Q
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, HTML, ButtonHolder

# def handle_uploaded_file:
#     with open('some/file/name.txt', 'wb+') as destination:
#     for chunk in f.chunks():
#         destination.write(chunk)


def write_sequence_file(sequence: str):
    """ Validate protein sequence"""
    tmp_seq = tempfile.NamedTemporaryFile(mode="wb+", delete=False)

    if len(str(sequence.strip())) == 0:
        raise forms.ValidationError(NEEDLE_CORRECT_SEQ_ERROR_MSG)

    if str(sequence).strip()[0] != ">":
        tmp_seq.write(">seq1\n".encode())

    tmp_seq.write(sequence.encode())
    tmp_seq.close()

    return tmp_seq.name


def is_fasta(content):
    fasta = SeqIO.parse(content, "fasta")
    return any(fasta)


def guess_if_protein(seq, thresh=0.99):
    """Guess if the given sequence is Protein."""
    # protein_letters = ['C', 'D', 'S', 'Q', 'K','I','P','T','F','N','G',
    #                'H','L','R','W','A','V','E','Y','M']
    protein_letters = ['A', 'C', 'G', 'T']
    # import pudb
    # pu.db
    for record in SeqIO.parse(seq, "fasta"):
        seq = record.seq

    seq = seq.upper()
    protein_alpha_count = 0
    for letter in protein_letters:
        protein_alpha_count += seq.count(letter)

    return (len(seq) == 0 or float(protein_alpha_count) / float(len(seq)) >= thresh)


class UserDataForm(forms.Form):

    userdata = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Paste your fasta sequence'}),
        required=False, label="User Data"
    )

    userfile = forms.FileField(
        label='or Select a fasta file to upload',
        required=False,
        # help_text='max. 42 megabytes',
    )

    def __init__(self, *args, session=None, **kwargs):
        self.session = session
        super().__init__(*args, **kwargs)
        self.fields['userdata'].widget.attrs['cols'] = 50
        self.helper = FormHelper()
        self.helper.form_id = 'id-UserDataForm'
        self.helper.form_class = 'UserDataForm'
        self.helper.form_method = 'post'
        self.helper.form_action = 'view_cart'
        self.helper.add_input(Submit('submit', 'Add to Cart'))

    def clean(self):
        userfile = self.cleaned_data.get('userfile')
        userdata = self.cleaned_data.get('userdata')

        if userfile:
            content = userfile.read().decode().strip()
        elif userdata:
            content = userdata
        else:
            raise forms.ValidationError('Please provide at least one field')

        if userfile and userdata:
            raise forms.ValidationError('Please use only one field')

        userdata = write_sequence_file(content)

        fasta = is_fasta(userdata)

        if fasta:
            dna = guess_if_protein(userdata)

        else:
            raise forms.ValidationError(
                "Please paste valid fasta sequence file")

        if not dna:
            for rec in SeqIO.parse(userdata, "fasta"):
                name = rec.id
                sequence = str(rec.seq)
                UserUploadData.objects.create(
                    session_key=self.session.session_key, name=name, sequence=sequence)

        else:
            raise forms.ValidationError(
                "Please provide valid protein sequence file")

        # return self.protein


class AnalysisForm(forms.Form):

    list_names = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    list_nterminal = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    list_middle = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    list_cterminal = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    userdataids = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )
    tool = forms.ChoiceField(required=False,
                             choices=[('clustal', 'Clustal')])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['sequence_in_form'].label = ''
        self.helper = FormHelper()
        self.helper.form_id = 'id-UserDataForm'
        self.helper.form_class = 'UserDataForm'
        self.helper.form_method = 'post'
        self.helper.form_action = 'domain_analysis'
        self.helper.add_input(Submit('submit', 'Submit'))

    def clean_userdataids(self):
        self.userdata = self.cleaned_data.get('userdataids', [])
        if self.userdata:
            self.userdata = [int(s) for s in self.userdata.split(',')]
        return self.userdata

    def clean(self):
        self.combined_selection = []
        try:
            self.selected_values = ast.literal_eval(
                self.cleaned_data.get('list_names'))
        except:
            self.selected_values = []

        try:
            self.list_nterminal = ast.literal_eval(
                self.cleaned_data.get('list_nterminal'))
        except:
            self.list_nterminal = []

        try:
            self.list_cterminal = ast.literal_eval(
                self.cleaned_data.get('list_cterminal'))
        except:
            self.list_cterminal = []

        try:
            self.list_middle = ast.literal_eval(
                self.cleaned_data.get('list_middle'))
        except:
            self.list_middle = []

        if self.list_nterminal:
            self.combined_selection += self.list_nterminal
        if self.list_middle:
            self.combined_selection += self.list_middle
        if self.list_cterminal:
            self.combined_selection += self.list_cterminal
        if self.selected_values:
            self.combined_selection += self.selected_values

        if len(self.combined_selection) <= 3:
            raise forms.ValidationError(
                "Select more than three sequences for the analysis")
        elif self.combined_selection:
            self.combined_selection = list(set(self.combined_selection))
        else:
            raise forms.ValidationError(
                "Make some selection to do the analysis")

        # if not self.combined_selection:
        #     raise forms.ValidationError('Select some sequences')
        # if self.count_number_lines() <= 3:
        #     raise forms.ValidationError(
        #         'Please select more than three sequences')

        return self.cleaned_data

    def save(self):
        self.write_files_for_clustal()
        self.protein_detail_data()
        self.write_input_file_clustal()
        self.count_number_lines()

        return self.clustalomega_in_tmp.name, self.guidetree_out_tmp.name, self.num_lines

    def count_number_lines(self):
        self.num_lines = sum(1 for line in open(
            self.clustalomega_in_tmp.name) if line.startswith(">"))

    def write_files_for_clustal(self):
        """ Validate protein sequence """
        self.clustalomega_in_tmp = tempfile.NamedTemporaryFile(
            mode="wb+", delete=False)
        self.clustalomega_out_tmp = tempfile.NamedTemporaryFile(
            mode="wb+", delete=False)
        self.guidetree_out_tmp = tempfile.NamedTemporaryFile(
            mode="wb+", delete=False)

    def protein_detail_data(self):
        self.accession = {}

        self.data = \
            PesticidalProteinDatabase.objects.filter(
                name__in=self.combined_selection)
        if self.data:
            for item in self.data:
                self.accession[item.accession] = item

        self.protein_detail = ProteinDetail.objects.filter(
            accession__in=list(self.accession.keys()))

    def write_input_file_clustal(self):
        userdata = UserUploadData.objects.filter(
            pk__in=self.userdata)

        with open(self.clustalomega_in_tmp.name, 'wb') as temp:
            for item in self.data:
                output = ''
                item_name = item.name
                if item.name in self.list_nterminal:
                    nterminal = [
                        protein for protein in self.protein_detail if protein.accession == item.accession]
                    item_name += '_1'
                    for item1 in nterminal:
                        output += item1.get_endotoxin_n()
                        # for line in output:
                        #     if line.startswith('>'):
                        #         line = line + '_1'
                if item.name in self.list_cterminal:
                    cterminal = [
                        protein for protein in self.protein_detail if protein.accession == item.accession]
                    for item1 in cterminal:
                        output += item1.get_endotoxin_c()
                    item_name += '_2'
                if item.name in self.list_middle:
                    middle = [
                        protein for protein in self.protein_detail if protein.accession == item.accession]
                    for item1 in middle:
                        output += item1.get_endotoxin_m()
                else:
                    fasta = textwrap.fill(item.sequence, 80)
                    str_to_write = f">{item_name}\n{fasta}\n"
                    temp.write(str_to_write.encode())

                if output:
                    str_to_write = f">{item.name}\n{output}\n"
                    temp.write(str_to_write.encode())

            for item in userdata:
                fasta = textwrap.fill(item.sequence, 80)
                if len(item.name) > 10:
                    item.name = item.name[:10]
                str_to_write = f">{item.name}\n{fasta}\n"
                temp.write(str_to_write.encode())


class DendogramForm(forms.Form):

    category_type = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices='',
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(DendogramForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-dendogram'
        self.helper.form_class = 'dendogramForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'dendogram_celery'

        self.helper.add_input(Submit('submit', 'Submit'))

        categories = \
            PesticidalProteinDatabase.objects.order_by(
                'name').values_list('name', flat=True)
        self.category_prefixes = {}
        self.category_options = [('all', 'All')]
        for category in categories:
            prefix = category[0:3]
            self.category_prefixes[prefix.lower()] = prefix.title()
        self.category_options.extend(
            sorted(self.category_prefixes.items(), key=lambda x: x[0][:3]))

        self.fields['category_type'].choices = self.category_options
        self.fields['category_type'].label = ''

    def clean(self):
        self.open_files_for_clustal()
        self.filter_categories()
        self.write_input_file_clustal()
        self.count_number_lines()

        if self.numlines < 3:
            raise forms.ValidationError(
                "At least three or more sequences are needed")

    def save(self):
        # self.run_clustal()
        return self.clustalomega_in_tmp.name, self.guidetree_out_tmp.name

    def count_number_lines(self):
        self.numlines = sum(1 for line in open(
            self.clustalomega_in_tmp.name) if line.startswith(">"))

        # if self.num_lines <= 3:
        #     raise forms.ValidationError(
        #         "Atleast three or more sequences aare needed.This category has less than 3")

    def open_files_for_clustal(self):
        """ open files for clustal """
        self.clustalomega_in_tmp = tempfile.NamedTemporaryFile(
            mode="wb+", delete=False)
        self.clustalomega_out_tmp = tempfile.NamedTemporaryFile(
            mode="wb+", delete=False)
        self.guidetree_out_tmp = tempfile.NamedTemporaryFile(
            mode="wb+", delete=False)

    def filter_categories(self):
        """ """
        self.category_type = self.cleaned_data.get('category_type')
        self.data = PesticidalProteinDatabase.objects.none()
        for category in self.category_type:
            if category == 'all':
                self.data |= PesticidalProteinDatabase.objects.all()
                print(self.data)
            else:
                self.data |= PesticidalProteinDatabase.objects.filter(
                    name__istartswith=category)

    def write_input_file_clustal(self):
        """ """
        str_to_write = b''
        with open(self.clustalomega_in_tmp.name, 'wb') as temp:
            for category in self.category_type:
                if category == 'all':
                    for item in self.data:
                        str_to_write = f">{item.name}\n{item.sequence}\n"
                        lines = str_to_write.count('\n')
                        temp.write(str_to_write.encode())
                else:
                    for item in self.data:
                        for category in self.category_type:
                            if category.capitalize() in item.name:
                                str_to_write = f">{item.name}\n{item.sequence}\n"
                                lines = str_to_write.count('\n')
                                temp.write(str_to_write.encode())

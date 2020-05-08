import tempfile
import textwrap
import subprocess
import ast
from Bio.Align.Applications import ClustalOmegaCommandline
from database.models import PesticidalProteinDatabase, UserUploadData, ProteinDetail
from django import forms
from django.forms import widgets
from django.db.models import Q
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class AnalysisForm(forms.Form):

    session_list_names = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    session_list_nterminal = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    session_list_middle = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    session_list_cterminal = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    userdataids = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    def clean_userdataids(self):

        self.userdata = self.cleaned_data.get('userdataids', [])

        if self.userdata:
            self.userdata = [int(s) for s in self.userdata.split(',')]

    def clean_session_list_names(self):
        try:
            self.selected_values_1 = ast.literal_eval(
                self.cleaned_data.get('session_list_names'))
        except Exception:
            self.selected_values_1 = []
        # self.selected_values_1 = self.cleaned_data['session_list_names']

        # if not self.selected_values_1:
            # HiddenInput does not produce any validation error how to fix this
        #     raise forms.ValidationError('Select some sequences')
        # elif len(self.selected_values_1) <= 3:
        #     raise forms.ValidationError(
        #         "Select atleast more than two sequences")
        # return self.selected_values_1

    # def clean_session_list_nterminal(self):
    #     self.list_nterminal = ast.literal_eval(
    #         self.cleaned_data.get('session_list_nterminal'))
    #
    # def clean_session_list_cterminal(self):
    #     self.list_cterminal = ast.literal_eval(
    #         self.cleaned_data.get('session_list_cterminal'))
    #
    # def clean_session_list_middle(self):
    #     self.list_middle = ast.literal_eval(
    #         self.cleaned_data.get('session_list_middle'))

    def clean(self):
        try:
            self.list_nterminal = ast.literal_eval(
                self.cleaned_data.get('session_list_nterminal'))
        except:
            self.list_nterminal = []

        try:
            self.list_cterminal = ast.literal_eval(
                self.cleaned_data.get('session_list_cterminal'))
        except:
            self.list_cterminal = []

        try:
            self.list_middle = ast.literal_eval(
                self.cleaned_data.get('session_list_middle'))
        except:
            self.list_middle = []
        # self.list_nterminal = self.cleaned_data['session_list_nterminal']
        # self.list_cterminal = self.cleaned_data['session_list_cterminal']
        # self.list_middle = self.cleaned_data['session_list_middle']

        # print("type")

        # combine all selection
        self.combined_selection = self.list_nterminal + \
            self.list_cterminal + self.list_middle + self.selected_values_1
        # print("type", type(self.combined_selection))
        # print("type", self.combined_selection)

        # print("values", self.combined_selection)
        # print("type", type(self.combined_selection))

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
        # print(self.data)

    def write_input_file_clustal(self):
        userdata = UserUploadData.objects.filter(
            pk__in=self.userdata)

        with open(self.clustalomega_in_tmp.name, 'wb') as temp:
            for item in self.data:
                output = ''
                if item.name in self.list_nterminal:
                    nterminal = [
                        protein for protein in self.protein_detail if protein.accession == item.accession]
                    for item1 in nterminal:
                        output += item1.get_endotoxin_n()
                if item.name in self.list_cterminal:
                    cterminal = [
                        protein for protein in self.protein_detail if protein.accession == item.accession]
                    for item1 in cterminal:
                        output += item1.get_endotoxin_c()
                if item.name in self.list_middle:
                    # print('middle loop running')
                    # print(item.name)
                    middle = [
                        protein for protein in self.protein_detail if protein.accession == item.accession]
                    for item1 in middle:
                        output += item1.get_endotoxin_m()
                else:
                    # print("item", item)
                    fasta = textwrap.fill(item.sequence, 80)
                    str_to_write = f">{item.name}\n{fasta}\n"
                    temp.write(str_to_write.encode())

                if output:
                    # print('middle domain')
                    # print(output)
                    str_to_write = f">{item.name}\n{output}\n"
                    temp.write(str_to_write.encode())

            for item in userdata:
                fasta = textwrap.fill(item.sequence, 80)
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
        self.category_options = [('all', 'ALL')]
        for category in categories:
            prefix = category[0:3]
            self.category_prefixes[prefix.lower()] = prefix.upper()
        self.category_options.extend(
            sorted(self.category_prefixes.items(), key=lambda x: x[0][:3]))

        self.fields['category_type'].choices = self.category_options
        self.fields['category_type'].label = 'Category Types'

    def save(self):
        self.open_files_for_clustal()
        self.filter_categories()
        self.write_input_file_clustal()
        self.count_number_lines()
        # self.run_clustal()
        return self.clustalomega_in_tmp.name, self.guidetree_out_tmp.name, self.num_lines

    def count_number_lines(self):
        self.num_lines = sum(1 for line in open(
            self.clustalomega_in_tmp.name) if line.startswith(">"))

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

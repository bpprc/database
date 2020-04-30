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
        self.selected_values_1 = ast.literal_eval(
            self.cleaned_data.get('session_list_names'))

        if not self.selected_values_1:
            # HiddenInput does not produce any validation error how to fix this
            raise forms.ValidationError('Select some sequences')
        elif len(self.selected_values_1) <= 3:
            raise forms.ValidationError(
                "Select atleast more than two sequences")
        return self.selected_values_1

    def clean(self):
        self.list_nterminal = self.cleaned_data['session_list_nterminal']
        self.list_cterminal = self.cleaned_data['session_list_cterminal']
        self.list_middle = self.cleaned_data['session_list_middle']
        # print("The nterminal: ", self.list_nterminal)
        # print("The middle domain:", self.list_middle)
        # print("The cterminal domain", self.list_cterminal)

    def save(self):
        print('i am save function')
        self.write_files_for_clustal()
        self.protein_detail_data()
        self.write_input_file_clustal()

        return self.clustalomega_in_tmp.name, self.guidetree_out_tmp.name

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
        # self.filtered_cry = list(
        #     filter(lambda x: x[0:3] == 'Cry', self.selected_values_1))
        # self.unique_cry = [
        #     elem for elem in self.filtered_cry if elem not in self.list_nterminal]

        # self.common_cry = lists(set(self.filtered_cry)).intersection(self.list_nterminal)
        #
        # self.filtered_non_cry = list(
        #     filter(lambda x: x[0:3] != 'Cry', self.selected_values_1))
        self.data = \
            PesticidalProteinDatabase.objects.filter(
                name__in=self.selected_values_1)
        if self.data:
            for item in self.data:
                self.accession[item.accession] = item

        self.protein_detail = ProteinDetail.objects.filter(
            accession__in=list(self.accession.keys()))

    def write_input_file_clustal(self):
        print('i am write file for clustal function')
        # data = \
        #     PesticidalProteinDatabase.objects.filter(
        #         name__in=self.selected_values_1)

        # unique_cry = \
        #     PesticidalProteinDatabase.objects.filter(
        #         name__in=self.unique_cry)
        #
        # cry = \
        #     PesticidalProteinDatabase.objects.filter(
        #         name__in=self.filtered_cry)
        # unique_nterminal = \
        #     PesticidalProteinDatabase.objects.filter(
        #         name__in=self.list_nterminal)
        #
        # unique_middle = \
        #     PesticidalProteinDatabase.objects.filter(
        #         name__in=self.list_middle)
        #
        # unique_cterminal = \
        #     PesticidalProteinDatabase.objects.filter(
        #         name__in=self.list_cterminal)

        userdata = UserUploadData.objects.filter(
            pk__in=self.userdata)

        with open(self.clustalomega_in_tmp.name, 'wb') as temp:
            # for protein in cry:
            # output = ''
            # if protein in self.list_nterminal:
            #     output += protein.get_endotoxin_n()

            # k = [item for item in self.data if item.name in self.list_nterminal]

            for item in self.data:
                # output = ''
                # if item.name in self.list_nterminal:
                #     nterminal = [
                #         protein for protein in self.protein_detail if protein.accession == item.accession]
                #     for item1 in nterminal:
                #         try:
                #             output += item1.get_endotoxin_n()
                #             # output = textwrap.fill(output, 80)
                #         except:
                #             print("item", item)
                #             pass
                #
                # else:
                fasta = textwrap.fill(item.sequence, 80)
                str_to_write = f">{item.name}\n{fasta}\n"
                temp.write(str_to_write.encode())

            for item in userdata:
                fasta = textwrap.fill(item.sequence, 80)
                str_to_write = f">{item.name}\n{fasta}\n"
                temp.write(str_to_write.encode())


class DendogramForm(forms.Form):

    category_type = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices='',
        required=True
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
        self.fields['category_type'].label = 'Category types'

    def save(self):
        self.open_files_for_clustal()
        self.filter_categories()
        self.write_input_file_clustal()
        # self.run_clustal()
        return self.clustalomega_in_tmp.name, self.guidetree_out_tmp.name, self.newlines

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
        self.newlines = ''
        with open(self.clustalomega_in_tmp.name, 'wb') as temp:
            for category in self.category_type:
                if category == 'all':
                    for item in self.data:
                        str_to_write = f">{item.name}\n{item.sequence}\n"
                        lines = str_to_write.count('\n')
                        self.newlines = lines
                        temp.write(str_to_write.encode())
                else:
                    for item in self.data:
                        for category in self.category_type:
                            if category.capitalize() in item.name:
                                str_to_write = f">{item.name}\n{item.sequence}\n"
                                lines = str_to_write.count('\n')
                                self.newlines = lines
                                temp.write(str_to_write.encode())

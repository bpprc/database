import tempfile
import textwrap
import subprocess
import ast
from Bio.Align.Applications import ClustalOmegaCommandline
from database.models import PesticidalProteinDatabase, UserUploadData, ProteinDetail
from django import forms
from django.forms import widgets
from django.db.models import Q
from ete3 import Tree, TreeStyle, faces



class AnalysisForm(forms.Form):
    OPTIONS = (
        ('n-terminal domain', 'N-TERMINAL DOMAIN'),
        ('c-terminal domain', 'C-TERMINAL DOMAIN'),
        ('m-terminal domain', 'M-TERMINAL DOMAIN'),
        ('full length', 'FULL LENGTH'),
    )
    # domain_type = forms.CharField(widget=forms.Select(choices=OPTIONS))
    domain_type = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=OPTIONS)
    session_list_names = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['domain_type'].label = ''

    def clean_session_list_names(self):
        self.selected_values_1 = ast.literal_eval(self.cleaned_data.get('session_list_names'))

        if not self.selected_values_1:
            raise forms.ValidationError('Select some sequences')  #HiddenInput does not produce any validation error how to fix this
        elif len(self.selected_values_1) <= 2:
            raise forms.ValidationError("Select atleast more than two sequences")
        return self.selected_values_1

    def clean(self):
        data = self.cleaned_data
        # self.selected_values_1 = ast.literal_eval(self.cleaned_data.get('session_list_names'))
        # self.selected_values_1 = eval(self.cleaned_data.get('session_list_names', '[]'))
        # print(self.selected_values_1, type(self.selected_values_1))

        if not self.selected_values_1:
            raise forms.ValidationError('Select some sequences')  #HiddenInput does not produce any validation error how to fix this
        elif len(self.selected_values_1) <= 2:
            raise forms.ValidationError("Select atleast more than two sequences")
        return data

    def clean_domain_type(self):
        self.domain_type = self.cleaned_data.get('domain_type') #what are things clean data check by default in django?
        if not self.domain_type:
            raise ValidationError("Select any domain") #How do you setup defaul values to a filed? for example N-terminal domain
        return self.domain_type

    def save(self):
        self.write_files_for_clustal()
        self.filtered_three_domains()
        self.protein_detail_data()
        self.write_input_file_clustal()
        self.run_clustal()
        return self.rooted_tree

    def write_files_for_clustal(self):
        """ Validate protein sequence """
        self.clustalomega_in_tmp = tempfile.NamedTemporaryFile(mode="wb+", delete=False)
        self.clustalomega_out_tmp = tempfile.NamedTemporaryFile(mode="wb+", delete=False)
        self.guidetree_out_tmp = tempfile.NamedTemporaryFile(mode="wb+", delete=False)
        # print(self.clustalomega_in_tmp.name)
        # print(self.guidetree_out_tmp.name)
        # print(self.clustalomega_out_tmp.name)

    def filtered_three_domains(self):
        self.filtered_cry = []
        if self.selected_values_1:
            for name in self.selected_values_1:
                if name[0:3] == 'Cry':
                    self.filtered_cry.append(name)

    def protein_detail_data(self):
        self.accession = {}
        data = \
            PesticidalProteinDatabase.objects.filter(name__in=self.filtered_cry)
        if data:
            for item in data:
                self.accession[item.accession] = item

        self.protein_detail = ProteinDetail.objects.filter(accession__in=list(self.accession.keys()))

    def write_input_file_clustal(self):
        output = ''
        with open(self.clustalomega_in_tmp.name, 'wb') as temp:
            for protein in self.protein_detail:
                if 'm-terminal domain' in self.domain_type:
                    output += protein.get_endotoxin_m()
                if 'n-terminal domain' in self.domain_type:
                    output += protein.get_endotoxin_n()
                if 'c-terminal domain' in self.domain_type:
                    output += protein.get_endotoxin_c()
                if 'full length' in self.domain_type:
                    output += protein.get_endotoxin_m()
                    output += protein.get_endotoxin_n()
                    output += protein.get_endotoxin_c()
                output = textwrap.fill(output, 80)
                protein_data = self.accession[protein.accession]
                str_to_write = f">{protein_data.name}\n{output}\n"
                temp.write(str_to_write.encode())

    def cmd(self, command):
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )
        out, error = process.communicate()

    def run_clustal(self):
        cmd = 'clustalo -i '+ self.clustalomega_in_tmp.name+ ' -o ' + self.clustalomega_out_tmp.name +' --guidetree-out='+self.guidetree_out_tmp.name + ' --force'
        self.cmd(cmd)
        self.rooted_tree = Tree(self.guidetree_out_tmp.name, quoted_node_names=True, format=1)



class DendogramForm(forms.Form):
    OPTIONS = (
        ('app', 'APP'),
        ('cry', 'CRY'),
        ('cyt', 'CYT'),
        ('mpp', 'MPP'),
        ('mcf', 'MCF'),
        ('mtx', 'MTX'),
        ('tpp', 'TPP'),
        ('gpp', 'GPP'),
        ('vip', 'VIP'),
        ('vpa', 'VPA'),
        ('vpb', 'VPB'),
        ('xpp', 'XPP'),
        ('all', 'ALL'),
    )

    # category_type = forms.CharField(widget=forms.Select(choices=(OPTIONS)))
    category_type = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=OPTIONS)
    # print(type(category_type))
    # django model choice field

    def categories(self):

        categories = \
            PesticidalProteinDatabase.objects.order_by(
                'name').values_list('name').distinct()
        self.category_prefixes = []
        for category in categories:
            prefix = category[0][:3]
            if prefix not in self.category_prefixes:
                self.category_prefixes.append(prefix)
        self.category_prefixes.append('all')

    def options(self):
        category_prefixes_uppercase = [prefix.upper() for prefix in self.category_prefixes]
        self.OPTIONS = zip(self.category_prefixes, category_prefixes)
        print('options', self.OPTIONS)

    def save(self):
        self.open_files_for_clustal()
        self.filter_categories()
        self.write_input_file_clustal()
        self.run_clustal()
        return self.rooted_tree

    def open_files_for_clustal(self):
        """ open files for clustal """
        self.clustalomega_in_tmp = tempfile.NamedTemporaryFile(mode="wb+", delete=False)
        self.clustalomega_out_tmp = tempfile.NamedTemporaryFile(mode="wb+", delete=False)
        self.guidetree_out_tmp = tempfile.NamedTemporaryFile(mode="wb+", delete=False)
        # print("input file", self.clustalomega_in_tmp.name)
        # print("output file", self.clustalomega_out_tmp.name)
        # print('guidetree', self.guidetree_out_tmp.name)

    def filter_categories(self):
        """ """
        self.category_type = self.cleaned_data.get('category_type')
        print(self.category_type)
        print(type(self.category_type))
        for category in self.category_type:
            if category == 'all':
                context = {
                    'proteins': PesticidalProteinDatabase.objects.all()
                }
                self.data = list(context.get('proteins'))

            else:
                self.data = PesticidalProteinDatabase.objects.filter(name__istartswith=category)
            # filtered_type = Q()
            # for type in self.category_type:
            #     print(type.name)
            #     filtered_type = filtered_type | Q(name=type)
            # self.data = PesticidalProteinDatabase.objects.filter(name__in=filtered_type)

    def write_input_file_clustal(self):
        """ """
        str_to_write = b''
        with open(self.clustalomega_in_tmp.name, 'wb') as temp:
            for category in self.category_type:
                if category == 'all':
                    for item in self.data:
                        str_to_write = f">{item.name}\n{item.fastasequence}\n"
                        temp.write(str_to_write.encode())
                else:
                    for item in self.data:
                        for category in self.category_type:
                            if category.capitalize() in item.name:
                                str_to_write = f">{item.name}\n{item.fastasequence}\n"
                                temp.write(str_to_write.encode())


    def cmd(self, command):
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )
        out, error = process.communicate()

    def run_clustal(self):
        cmd = 'clustalo -i '+ self.clustalomega_in_tmp.name+' --guidetree-out='+self.guidetree_out_tmp.name + ' --force'
        self.cmd(cmd)
        self.rooted_tree = Tree(self.guidetree_out_tmp.name, quoted_node_names=True, format=1)
        print(self.rooted_tree)

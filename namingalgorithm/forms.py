"""Sequence submission form."""

from django import forms
from django.forms import modelformset_factory
from .models import UserSubmission
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, HTML, ButtonHolder
# from crispy_forms.bootstrap import AppendedText

RECAPTCHA_PUBLIC_KEY = "6Lc-HfMUAAAAALHi0-vkno4ntkJvLW3rAF-d5UXT"


# class CustomToxinBox(Field):
#     template = 'namingalgorithm/toxinbox.html'

class UserSubmissionForm(forms.ModelForm):
    class Meta:
        model = UserSubmission
        fields = ['submittersname', 'submittersemail', 'proteinname', 'proteinname', 'proteinsequence', 'bacterium', 'bacterium_textbox', 'taxonid',
                  'year', 'accessionnumber', 'partnerprotein', 'partnerprotein_textbox', 'toxicto', 'nontoxic', 'dnasequence', 'pdbcode', 'publication', 'comment', ]


ToxicToFormSet = modelformset_factory(
    UserSubmission,
    fields=('toxicto',),
    extra=1,
    widgets={'toxicto': forms.TextInput(attrs={
        'placeholder': 'Toxic to'
    })
    }
)
# class UserSubmissionForm(forms.ModelForm):
#     """Sequence submission form."""
#     submittersname = forms.CharField(
#         label="Submitter's Name",
#         widget=forms.TextInput(
#             attrs={'placeholder': 'Nancy Sanders'})
#     )
#
#     submittersemail = forms.CharField(
#         label="Submitter's Email",
#         widget=forms.TextInput(
#             attrs={'placeholder': 'contact@bpprc.org'})
#     )
#
#     proteinsname = forms.CharField(
#         label='Current Protein Name',
#         widget=forms.TextInput(
#             attrs={'placeholder': 'CryE1'}),
#         required=False
#     )
#
#     year = forms.CharField(
#         label='Year',
#         widget=forms.TextInput(
#             attrs={'placeholder': '2020'}),
#         required=False
#     )
#     proteinsequence = forms.CharField(
#         label='Protein Sequence',
#         widget=forms.Textarea(
#             attrs={'placeholder': ">ABI14444.1 Cry51Aa1 [Bacillus thuringiensis F14-1] MIFLAILDLKSLVLNAINYWGPKNNNGIQGGDFGYPISEKQIDTSIITSTHPRLIPHDLTIPQNLETIFTTTQVLTNNTDLQQSQTVSFAKKTTTTTSTSTTNGWTEGGKISDTLEEKVSVSIPFIGEGGGKNSTTIEANFAHNSSTTTFQQASTDIEWNISQPVLVPPRKQVVATLVIMGGNFTIPMDLMTTIDSTEHYSGYPILTWISSPDNSYNGPFMSWYFANWPNLPSGFGPLNSDNTVTYTGSVVSQVSAGVYATVRFDQYDIHNLRTIEKTWYARHATLHNGKKISINNVTEMAPTSPIKTN "}),
#         required=False
#     )
#
#     bacterium = forms.ChoiceField(
#         choices=((True, "Yes"), (False, "No")),
#         label='Bacterium',
#         widget=forms.RadioSelect(
#             attrs={'placeholder': 'Nancy Sanders'}
#         ),
#         initial=True,
#         required=False,
#     )
#
#     bacterium_textbox = forms.CharField(
#         label='Name of source bacterium (ideally taxonid)',
#         widget=forms.TextInput(
#             attrs={'placeholder': ''})
#     )
#
#     accessionnumber = forms.CharField(
#         label='Genbank accession Number',
#         widget=forms.TextInput(
#             attrs={'placeholder': 'ABC12345'}),
#         required=True
#     )
#
#     dnasequence = forms.CharField(
#         label='DNA Sequence',
#         widget=forms.Textarea(
#             attrs={'placeholder': ">DQ836184.1 Bacillus thuringiensis strain F14-1 Cry51Aa1 (cry51Aa1) gene, complete cds \
#             ATGATTTTTTTGGCAATTTTAGATTTAAAATCTTTAGTACTCAATGCAATAAATTATTGGGGTCCTAAAAATAATAATGGCATACAGGGTGGTGATTTTGGTTACCCTATATCAGAAAAACAAATAGATACGTCTATTATAACTTCTACTCATCCTCGTTTAATTCCACATGATTTAACAATTCCTCAAAATTTAGAAACTATTTTTACTACAACTCAAGTATTAACAAATAATACAGATTTACAACAAAGTCAAACTGTTTCTTTTGCTAAAAAAACAACGACAACAACTTCAACTTCAACTACAAATGGTTGGACAGAAGGTGGGAAAATTTCAGATACATTAGAAGAAAAAGTAAGTGTATCTATTCCTTTTATTGGAGAGGGAGGAGGAAAAAACAGTACAACTATAGAAGCTAATTTTGCACATAACTCTAGTACTACTACTTTTCAACAGGCTTCAACTGATATAGAGTGGAATATTTCACAACCAGTATTGGTTCCCCCACGTAAACAAGTTGTAGCAACATTAGTTATTATGGGAGGTAATTTTACTATTCCTATGGATTTGATGACTACTATAGATTCTACAGAACATTATAGTGGTTATCCAATATTAACATGGATATCGAGCCCCGATAATAGTTATAATGGTCCATTTATGAGTTGGTATTTTGCAAATTGGCCCAATTTACCATCGGGGTTTGGTCCTTTAAATTCAGATAATACGGTCACTTATACAGGTTCTGTTGTAAGTCAAGTATCAGCTGGTGTATATGCCACTGTACGATTTGATCAATATGATATACACAATTTAAGGACAATTGAAAAAACTTGGTATGCACGACATGCAACTCTTCATAATGGAAAGAAAATATCTATAAATAATGTTACTGAAATGGCACCAACAAGTCCAATAAAAACAAATTAA "})
#     )
#
#     partnerprotein = forms.ChoiceField(
#         label='Partner Protein required for toxicity?',
#         choices=((True, "Yes"), (False, "No")),
#         widget=forms.RadioSelect(),
#         initial=False,
#         required=False,
#     )
#
#     partnerprotein_textbox = forms.CharField(
#         label='Partner Protein Name',
#         widget=forms.TextInput(
#             attrs={'placeholder': ''}),
#         required=False
#     )
#
#     toxicto = forms.CharField(
#         label='Toxic to',
#         widget=forms.TextInput(
#             attrs={'placeholder': ''}),
#         required=False
#     )
#
#     nontoxic = forms.CharField(
#         label='Nontoxic to',
#         widget=forms.TextInput(
#             attrs={'placeholder': ''}),
#         required=False
#     )
#     pdbcode = forms.CharField(
#         label='PDB code',
#         widget=forms.TextInput(
#             attrs={'placeholder': '5KUC'}),
#         required=False
#     )
#
#     publication = forms.CharField(
#         label='Publication',
#         widget=forms.Textarea(
#             attrs={'placeholder': ''}),
#         required=False
#     )
#
#     comment = forms.CharField(
#         label='Comments',
#         widget=forms.Textarea(
#             attrs={'placeholder': ''}),
#         required=False
#     )
# print(toxicto)

# def __init__(self, *args, **kwargs):
#     super(UserSubmissionForm, self).__init__(*args, **kwargs)
#
#     self.fields['proteinsequence'].widget.attrs['cols'] = 50
#     self.fields['proteinsequence'].widget.attrs['cols'] = 20
#     self.fields['bacterium_textbox'].widget.attrs['cols'] = 10
#     self.fields['comment'].widget.attrs['cols'] = 50
#     self.fields['comment'].widget.attrs['cols'] = 20
#
#     self.fields['toxicto'].label = 'Toxic to'
#     self.helper = FormHelper()
#     self.helper.form_id = 'id-UserSubmissionForm'
#     self.helper.form_class = 'UserSubmissionForm'
#     self.helper.form_method = 'post'
#     self.helper.form_action = 'submit'
#     self.helper.add_input(Submit('submit', 'Submit'))
#
#     self.helper.layout = Layout(
#         Row(
#             Column('submittersname',
#                    css_class='form-group col-md-6 mb-0'),
#             Column('submittersemail',
#                    css_class='form-group col-md-6 mb-0'),
#             css_class='form-row'
#         ),
#         Row(
#             Column('proteinsname',
#                    css_class='form-group col-md-10 mb-0'),
#             Column('year',
#                    css_class='form-group col-md-2 mb-0'),
#             css_class='form-row'
#         ),
#         Row(
#             Column('bacterium',
#                    css_class='form-group col-md-2 mb-0'),
#             Column('bacterium_textbox',
#                    css_class='form-group col-md-6 mb-0'),
#             # Column('taxonid',
#             #        css_class='form-group col-md-5 mb-0'),
#             css_class='form-row'
#         ),
#         Row(
#             Column('accessionnumber',
#                    css_class='form-group col-md-3 mb-0'),
#             css_class='form-row'
#         ),
#         'dnasequence',
#         'proteinsequence',
#         Row(
#             Column('partnerprotein',
#                    css_class='form-group col-md-3 mb-0'),
#             Column('partnerprotein_textbox',
#                    css_class='form-group col-md-9 mb-0'),
#             css_class='form-row'
#         ),
#         'toxicto',
#         'nontoxic',
#         'pdbcode',
#         'publication',
#         'comment',
#         HTML('<div class="form-group col-md-6"><div class="g-recaptcha" data-sitekey="%s"></div></div>' %
#              RECAPTCHA_PUBLIC_KEY),
# ButtonHolder(
#     Submit('submit', 'Submit')
# )

# )
#
# class Meta:
#     model = UserSubmission
#     fields = ['submittersname',
#               'submittersemail',
#               'proteinname',
#               'year',
#               'proteinsequence',
#               'bacterium',
#               'bacterium_textbox',
#               # 'taxonid',
#               'accessionnumber',
#               'dnasequence',
#               'partnerprotein',
#               'partnerprotein_textbox',
#               'toxicto',
#               'nontoxic',
#               'pdbcode',
#               'publication',
#               'comment']


#
#
# class ToxicFormSetHelper(FormHelper):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.form_method = 'post'
#         self.layout = Layout(
#             'toxicto'
#         )
#         self.render_required_fields = False

# from django import forms
# from django.core.exceptions import ValidationError
# from database.models import PesticidalProteinDatabase, Description
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit, Layout, Row, Column, HTML, ButtonHolder
# from crispy_forms.bootstrap import AppendedText
# from django.core.validators import MinLengthValidator
#
#
# class NeedleAPIForm(forms.Form):
#
#     sequence1_in_form = forms.CharField(
#         widget=forms.Textarea, required=False, label="Or user-supplied sequence 1 (plain or fasta format)")
#     protein_id2 = forms.ModelChoiceField(
#         queryset=PesticidalProteinDatabase.objects.all(), required=False, label="Database protein 2")
#     sequence2_in_form = forms.CharField(
#         widget=forms.Textarea, required=False, label="Or user-supplied sequence 2 (plain or fasta format)")
#     tool = forms.ChoiceField(required=False,
#                              choices=[('needle', 'Needle'), ('blastp', 'BLASTP')])
#     email = forms.EmailField(required=False, widget=forms.EmailInput())
#     type = forms.ChoiceField(required=False,
#                              choices=[('protein', 'Protein'), ('dna', 'DNA')])
#
#     def clean_sequence1_in_form(self):
#
#         sequence1_in_form = self.cleaned_data['sequence1_in_form']
#
#         if sequence1_in_form:
#             return write_sequence_file(sequence1_in_form)
#
#         return sequence1_in_form
#
#     def clean_sequence2_in_form(self):
#
#         sequence2_in_form = self.cleaned_data['sequence2_in_form']
#
#         if sequence2_in_form:
#             return write_sequence_file(sequence2_in_form)
#
#         return sequence2_in_form
#
#     def clean(self):
#         protein1 = self.cleaned_data['protein_id1']
#         protein2 = self.cleaned_data['protein_id2']
#         sequence1_in_form = self.cleaned_data['sequence1_in_form']
#         sequence2_in_form = self.cleaned_data['sequence2_in_form']
#
#         if sequence1_in_form:
#             sequence_is_protein = guess_if_protein(sequence1_in_form)
#             if sequence_is_protein:
#                 raise forms.ValidationError(
#                     "Currently, it supports only protein sequences")
#
#         if sequence2_in_form:
#             sequence_is_protein = guess_if_protein(sequence2_in_form)
#             if sequence_is_protein:
#                 raise forms.ValidationError(
#                     "Currently, it supports only protein sequences")
#
#         if protein1 and sequence1_in_form:
#             raise forms.ValidationError(
#                 'Please select only one of Sequence / Choice')
#         elif not protein1 and not sequence1_in_form:
#             raise forms.ValidationError(
#                 'Please select only one of Sequence / Choice')
#
#         if protein2 and sequence2_in_form:
#             raise forms.ValidationError(
#                 'Please select only one of Sequence / Choice')
#         elif not protein2 and not sequence2_in_form:
#             raise forms.ValidationError(
#                 'Please select only one of Sequence / Choice')
#
#         # if not sequence_is_protein1 and not sequence_is_protein2:
#         #     raise forms.ValidationError("Currently, it supports only protien sequences")
#
#         return self.cleaned_data

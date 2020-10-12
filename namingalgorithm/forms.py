"""Sequence submission form."""

from django import forms
from django.forms import modelformset_factory
from .models import UserSubmission, SendEmail
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, HTML, ButtonHolder
# from crispy_forms.bootstrap import AppendedText

RECAPTCHA_PUBLIC_KEY = "6Lc-HfMUAAAAALHi0-vkno4ntkJvLW3rAF-d5UXT"


# class CustomToxinBox(Field):
#     template = 'namingalgorithm/toxinbox.html'

class SendEmailForm(forms.ModelForm):
    """Sequence submission form."""
    submittersname = forms.CharField(
        label="Submitter's Name",
        widget=forms.TextInput(
            attrs={'placeholder': ''})
    )

    submittersemail = forms.CharField(
        label="Submitter's Email",
        widget=forms.TextInput(
            attrs={'placeholder': ''})
    )

    proteinname = forms.CharField(
        label='Protein Name',
        widget=forms.TextInput(
            attrs={'placeholder': ''}),
        required=False
    )

    message = forms.CharField(
        label='message',
        widget=forms.Textarea(
            attrs={'placeholder': ''}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(SendEmailForm, self).__init__(*args, **kwargs)

        self.fields['proteinname'].widget.attrs['cols'] = 50
        # self.fields['proteinsname'].widget.attrs['cols'] = 20
        self.fields['message'].widget.attrs['cols'] = 50
        # self.fields['message'].widget.attrs['cols'] = 20

        self.helper = FormHelper()
        self.helper.form_id = 'id-SendEmailForm'
        self.helper.form_class = 'SendEmailForm'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = SendEmail
        fields = "__all__"


class UserSubmissionForm(forms.ModelForm):
    """Sequence submission form."""
    submittersname = forms.CharField(
        label="Submitter's Name",
        widget=forms.TextInput(
            attrs={'placeholder': ''})
    )

    submittersemail = forms.CharField(
        label="Submitter's Email",
        widget=forms.TextInput(
            attrs={'placeholder': ''})
    )

    proteinsname = forms.CharField(
        label='Current Protein Name',
        widget=forms.TextInput(
            attrs={'placeholder': ''}),
        required=False
    )

    year = forms.CharField(
        label='Year',
        widget=forms.TextInput(
            attrs={'placeholder': ''}),
        required=False
    )
    proteinsequence = forms.CharField(
        label='Protein Sequence',
        widget=forms.Textarea(
            attrs={'placeholder': ""}),
        required=True
    )

    public_or_private = forms.TypedChoiceField(
        label='Do you require the sequence to be maintained privately?',
        coerce=lambda x: x == 'True',
        choices=(('', 'Select one option'), (False, 'Yes'), (True, 'No')),
        required=True
    )

    bacterium = forms.ChoiceField(
        choices=((True, "Yes"), (False, "No")),
        label='Bacterium',
        widget=forms.RadioSelect(
            attrs={'placeholder': ''}
        ),
        initial=True,
        required=False,
    )

    bacterium_textbox = forms.CharField(
        label='Name of source bacterium (ideally taxonid)',
        # label='',
        widget=forms.TextInput(
            attrs={'placeholder': ''})
    )

    accessionnumber = forms.CharField(
        label='Genbank accession Number',
        widget=forms.TextInput(
            attrs={'placeholder': ''}),
        required=True
    )

    dnasequence = forms.CharField(
        label='DNA Sequence',
        widget=forms.Textarea(
            attrs={'placeholder': ""})
    )

    partnerprotein = forms.ChoiceField(
        label='Partner Protein required for toxicity?',
        choices=((True, "Yes"), (False, "No")),
        widget=forms.RadioSelect(),
        initial=False,
        required=False,
    )

    partnerprotein_textbox = forms.CharField(
        label='Partner Protein Name',
        widget=forms.TextInput(
            attrs={'placeholder': ''}),
        required=False
    )

    toxicto = forms.CharField(
        label='Toxic to',
        widget=forms.TextInput(
            attrs={'placeholder': ''}),
        required=False
    )

    nontoxic = forms.CharField(
        label='Nontoxic to',
        widget=forms.TextInput(
            attrs={'placeholder': ''}),
        required=False
    )
    pdbcode = forms.CharField(
        label='PDB code',
        widget=forms.TextInput(
            attrs={'placeholder': ''}),
        required=False
    )

    publication = forms.CharField(
        label='Publication',
        widget=forms.Textarea(
            attrs={'placeholder': ''}),
        required=False
    )

    comment = forms.CharField(
        label='Comments',
        widget=forms.Textarea(
            attrs={'placeholder': ''}),
        required=False
    )

    terms_conditions = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'size': '10'}),
        label='Our service is provided "as is". We expressly disclaim all warranties with respect to the services. We make no warranties or guarantees whatsoever, express or implied, including, any implied warranties of mechantability or fitness for a particular purpose. We are not liable for any use of the services, or for any loss, claim, damage, or liability of any kind or nature which may arise from or in connection with this service or our storage of your submission.'
    )

    def __init__(self, *args, **kwargs):
        super(UserSubmissionForm, self).__init__(*args, **kwargs)

        self.fields['proteinsequence'].widget.attrs['cols'] = 50
        self.fields['proteinsequence'].widget.attrs['cols'] = 20
        self.fields['bacterium_textbox'].widget.attrs['cols'] = 10
        self.fields['comment'].widget.attrs['cols'] = 50
        self.fields['comment'].widget.attrs['cols'] = 20

        self.fields['toxicto'].label = 'Toxic to'
        self.helper = FormHelper()
        self.helper.form_id = 'id-UserSubmissionForm'
        self.helper.form_class = 'UserSubmissionForm'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit'
        self.helper.add_input(Submit('submit', 'Submit'))

        self.helper.layout = Layout(
            Row(
                Column('submittersname',
                       css_class='form-group col-md-6 mb-0'),
                Column('submittersemail',
                       css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('proteinsname',
                       css_class='form-group col-md-10 mb-0'),
                Column('year',
                       css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('bacterium',
                       css_class='form-group col-md-2 mb-0'),
                Column('bacterium_textbox',
                       css_class='form-group col-md-6 mb-0'),
                # Column('taxonid',
                #        css_class='form-group col-md-5 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('accessionnumber',
                       css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            'dnasequence',
            'proteinsequence',
            'public_or_private',
            Row(
                Column('partnerprotein',
                       css_class='form-group col-md-3 mb-0'),
                Column('partnerprotein_textbox',
                       css_class='form-group col-md-9 mb-0'),
                css_class='form-row'
            ),
            'toxicto',
            'nontoxic',
            'pdbcode',
            'publication',
            'comment',
            'terms_conditions',
            HTML('<div class="form-group col-md-6"><div class="g-recaptcha" data-sitekey="%s"></div></div>' %
                 RECAPTCHA_PUBLIC_KEY),
            # ButtonHolder(
            #     Submit('submit', 'Submit')
            # )

        )

    class Meta:
        model = UserSubmission
        fields = ['submittersname',
                  'submittersemail',
                  'proteinname',
                  'year',
                  'proteinsequence',
                  'public_or_private',
                  'bacterium',
                  'bacterium_textbox',
                  'accessionnumber',
                  'dnasequence',
                  'partnerprotein',
                  'partnerprotein_textbox',
                  'toxicto',
                  'nontoxic',
                  'pdbcode',
                  'publication',
                  'comment',
                  'terms_conditions']


# ToxicToFormSet = modelformset_factory(
#     UserSubmission,
#     fields=('toxicto',),
#     extra=1,
#     widgets={'name': forms.TextInput(attrs={
#         'placeholder': 'Toxic to'
#     })
#     }
#
#
# )
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

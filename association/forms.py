from django import forms
from django.core.exceptions import ValidationError
from database.models import PesticidalProteinDatabase, Description
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, HTML, ButtonHolder
from crispy_forms.bootstrap import AppendedText
from django.core.validators import MinLengthValidator


class SearchForm(forms.Form):

    SEARCH_CHOICES = (
        ('bioassay', 'Bioassay'),
    )

    search_term = forms.CharField(label="", required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Search'}))
    search_fields = forms.ChoiceField(choices=SEARCH_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search_term'].error_messages = {
            'required': 'Please type a protein name'}
        self.fields['search_term'].label = 'Search term'

        validators = [v for v in self.fields['search_term'].validators if not isinstance(
            v, MinLengthValidator)]
        min_length = 3
        validators.append(MinLengthValidator(min_length))
        # print(validators)
        self.fields['search_term'].validators = validators

        # self.fields['search_term'].min_length = 3
        self.fields['search_fields'].label = ''
        self.helper = FormHelper()
        self.helper.form_id = 'id-SearchForm'
        self.helper.form_class = 'SearchForm'
        self.helper.form_method = 'post'
        self.helper.form_action = 'search_database'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
            Row(
                Column('search_term',
                       css_class='form-group input-group-append col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('search_fields',
                       css_class='form-group col-md-6'),
                css_class='form-row'
            ),)

    # def clean_search_term(self):
    #     data = self.cleaned_data['search_term']
    #
    #     if data is None:
    #         raise ValidationError(
    #             "Please provide the keywords to search in the database")
    #     elif data != 'R1' and len(data) < 3:
    #         raise ValidationError(
    #             "Please keep the search term under 3 characters")
    #     return data

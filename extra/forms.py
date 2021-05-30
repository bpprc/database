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

from extra.models import Feedback

RECAPTCHA_PUBLIC_KEY = "6Lc-HfMUAAAAALHi0-vkno4ntkJvLW3rAF-d5UXT"


class FeedbackForm(forms.ModelForm):
    name = forms.CharField(
        label="Submitter's Name",
        widget=forms.TextInput(attrs={"placeholder": ""}),
        required=True,
    )

    subject = forms.CharField(
        label="Subject",
        widget=forms.TextInput(attrs={"placeholder": ""}),
        required=True,
    )

    email = forms.CharField(
        label="Email",
        widget=forms.TextInput(attrs={"placeholder": ""}),
        required=False,
    )

    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={"placeholder": ""}),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = "id-FeedbackForm"
        self.helper.form_class = "FeedbackForm"
        self.helper.form_method = "post"
        self.helper.form_action = "feedback_home"
        self.helper.add_input(Submit("submit", "Submit"))

        self.helper.layout = Layout(
            Row(
                Column("name", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("subject", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("email", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("message", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            HTML(
                '<div class="form-group col-md-6"><div class="g-recaptcha" data-sitekey="%s"></div></div>'
                % RECAPTCHA_PUBLIC_KEY
            ),
        )

    def clean_subject(self):
        subject = self.cleaned_data["subject"]

        try:
            if int(subject.isdigit()):
                raise forms.ValidationError("Subject doesn't accept numbers")
        except:
            pass

    def clean(self):
        name = self.cleaned_data["name"]
        # subject = self.cleaned_data['subject']
        message = self.cleaned_data["message"]
        email = self.cleaned_data["email"]

    class Meta:
        model = Feedback
        fields = [
            "name",
            "subject",
            "email",
            "message",
        ]


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")

    def signup(self, request, user):
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user

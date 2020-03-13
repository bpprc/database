"""Sequence submission form."""

from django import forms
from .models import UserSubmission


class UserSubmissionForm(forms.ModelForm):
    """Sequence submission form."""

    class Meta:
        model = UserSubmission
        fields = ['name', 'year', 'sequence', 'comment', 'email']
        fields_required = ['name', 'year', 'sequence', 'email']

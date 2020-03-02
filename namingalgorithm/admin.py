"""Submit the sequence by user and name of the protein is predicted."""

from django.contrib import admin
from django.utils.html import format_html
from .models import UserSubmission


class UserSubmissionAdmin(admin.ModelAdmin):

    """Submit the sequence by user and name of the protein is predicted."""

    search_fields = ['email']
    list_display = (
        'name',
        'email',
        'run_align_link',
        'align_results',
        'create_data',
        'refresh',
        )

    def run_align_link(self, obj):
        """Submit the sequence by user and name of the protein is predicted."""
        return format_html('<a href="/run_naming_algorithm/?fulltextarea={0}&submission_id={1}" target="_blank">Run Align</a>'.format(obj.fastasequence,
                           obj.id))

    def align_results(self, obj):
        """Submit the sequence by user and name of the protein is predicted."""
        if obj.alignresults:
            return format_html('<a href="/align_results/?submission_id={0}" target="_blank">View Result</a>'.format(obj.id))
        return ''

    def create_data(self, obj):
        """Submit the sequence by user and name of the protein is predicted."""
        return format_html('<a href="/admin/database/pesticidalproteindatabase/add/?name={0}&fastasequence={1}" target="_blank">Create Data</a>'.format(obj.predict_name,
                           obj.fastasequence))

    def refresh(self, obj):
        """Submit the sequence by user and name of the protein is predicted."""
        return format_html('<a href="/admin/namingalgorithm/usersubmission/">refresh</a>'
                           )

    run_align_link.allow_tags = True
    run_align_link.description = 'Run the align link for the submission'

    align_results.allow_tags = True
    align_results.description = 'View the align results'

    align_results.allow_tags = True
    align_results.description = 'Create new data in the database'


admin.site.register(UserSubmission, UserSubmissionAdmin)

"""Submit the sequence by user and name of the protein is predicted."""

from django.contrib import admin
from django.utils.html import format_html
from .models import UserSubmission, Archive, SendEmail
from django.shortcuts import render


class ArchiveAdmin(admin.ModelAdmin):
    pass


class UserSubmissionAdmin(admin.ModelAdmin):

    """Submit the sequence by user and name of the protein is predicted."""

    search_fields = ['submittersemail']
    list_display = (
        'submittersname',
        'submittersemail',
        'run_align_link',
        'align_results',
        'create_data',
        'refresh',
        'send_email',
        'uploaded',
    )

    def run_align_link(self, obj):
        if ">" in str(obj.proteinsequence).split('\n')[0]:
            obj.proteinsequence = '\n'.join(
                str(obj.proteinsequence).split('\n')[1:])

        """Submit the sequence by user and name of the protein is predicted."""
        return format_html('<a href="/run_naming_algorithm/?fulltextarea={0}&submission_id={1}" target="_blank">Run Align</a>'.format(obj.proteinsequence, obj.id))

    def align_results(self, obj):
        """Submit the sequence by user and name of the protein is predicted."""
        if obj.alignresults:
            return format_html('<a href="/align_results/?submission_id={0}" target="_blank">View Result</a>'.format(obj.id))
        return ''

    def create_data(self, obj):
        """Submit the sequence by user and name of the protein is predicted."""
        return format_html('<a href="/admin/database/pesticidalproteindatabase/add/?name={0}&proteinsequence={1}" target="_blank">Create Data</a>'.format(obj.predict_name or '', obj.proteinsequence))

    def refresh(self, obj):
        """Submit the sequence by user and name of the protein is predicted."""
        return format_html('<a href="/admin/namingalgorithm/usersubmission/">refresh</a>')

    def send_email(self, obj):
        return format_html('<a href="/admin/contact/?submittersname={0}&email={1}&proteinname={2}" target="_blank">Send Email</a>'.format(obj.submittersname, obj.submittersemail, obj.proteinname or ''))

    run_align_link.allow_tags = True
    run_align_link.description = 'Run the align link for the submission'

    align_results.allow_tags = True
    align_results.description = 'View the align results'

    align_results.allow_tags = True
    align_results.description = 'Create new data in the database'


class SendEmailAdmin(admin.ModelAdmin):
    list_display = (
        'submittersname',
        'submittersemail',
        'proteinname',
    )


class ArchiveAdmin(admin.ModelAdmin):
    search_fields = ('proteinname', 'year', 'submittersname',
                     'submittersemail')
    fields = ('submittersname','submittersemail','proteinname', 'year','proteinsequence','bacterium','bacterium_textbox','taxonid','accessionnumber','partnerprotein','partnerprotein_textbox','toxicto','nontoxic','dnasequence','pdbcode','publication','comment','uploaded','predict_name','alignresults','terms_conditions')
    list_display = ('proteinname', 'submittersname',
                     'submittersemail','uploaded',)
    ordering = ('uploaded',)

admin.site.register(UserSubmission, UserSubmissionAdmin)
admin.site.register(Archive, ArchiveAdmin)
admin.site.register(SendEmail, SendEmailAdmin)

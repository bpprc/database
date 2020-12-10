"""Submit the sequence by user and name of the protein is predicted."""

from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from .models import UserSubmission, Archive, SendEmail
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin.checks import BaseModelAdminChecks
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.admin import GenericStackedInline
from namingalgorithm.models import AuditEntry


@admin.register(AuditEntry)
class AuditEntryLogAdmin(admin.ModelAdmin):
    list_display = ['action', 'username', 'ip', ]
    list_filter = ['action', ]


class LogEntryAdmin(admin.ModelAdmin):
    readonly_fields = ('content_type',
                       'user',
                       'action_time',
                       'object_id',
                       'object_repr',
                       'action_flag',
                       'change_message'
                       )

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(LogEntryAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class ModelAdminLog(GenericStackedInline):
    model = LogEntry

    # All fields are read-only, obviously
    readonly_fields = fields = ["action_time", "user", "change_message"]
    # No extra fields so noone can add new logs
    extra = 0
    # No one can delete logs
    can_delete = False

    # This is a hackity hack! See below
    checks_class = BaseModelAdminChecks

    def change_message(self, obj):
        message = obj.get_change_message()
        return message


class ArchiveResource(resources.ModelResource):

    class Meta:
        model = Archive


class ArchiveAdmin(ImportExportModelAdmin):
    resource_class = ArchiveResource

    search_fields = ['submittersemail', 'submittersname']
    list_display = (
        'submittersname',
        'accession',
        'uploaded',
        'admin_user',
        'admin_comments',
    )

    inlines = [ModelAdminLog]


class UserSubmissionResource(resources.ModelResource):

    class Meta:
        model = UserSubmission


class UserSubmissionAdmin(ImportExportModelAdmin):
    resource_class = UserSubmissionResource

    """Submit the sequence by user and name of the protein is predicted."""

    search_fields = ['submittersemail', 'submittersname', 'accession']
    list_display = (
        'submittersname',
        'accession',
        'run_align_link',
        'create_data',
        'refresh',
        'send_email',
        'uploaded',
    )

    inlines = [ModelAdminLog]

    # def copy_to_public(self, obj):
    #     return format_html('<a href="/admin/database/pesticidalproteindatabase/add/?name={0}&sequence={1}&name={2}" target="_blank">Create Data</a>'.format(obj.predict_name or '', obj.sequence))

    def run_align_link(self, obj):
        if ">" in str(obj.sequence).split('\n')[0]:
            obj.sequence = '\n'.join(
                str(obj.sequence).split('\n')[1:])

        """Submit the sequence by user and name of the protein is predicted."""
        return format_html('<a href="/run_naming_algorithm/?fulltextarea={0}&submission_id={1}" target="_blank">Run Align</a>'.format(obj.sequence, obj.id))

    def align_results(self, obj):
        """Submit the sequence by user and name of the protein is predicted."""
        if obj.alignresults:
            return format_html('<a href="/align_results/?submission_id={0}" target="_blank">View Result</a>'.format(obj.id))
        return ''

    def create_data(self, obj):
        """Submit the sequence by user and name of the protein is predicted."""
        return format_html('<a href="/admin/database/pesticidalproteindatabase/add/?name={0}&sequence={1}" target="_blank">Create Data</a>'.format(obj.predict_name or '', obj.sequence))

    def refresh(self, obj):
        """Submit the sequence by user and name of the protein is predicted."""
        return format_html('<a href="/admin/namingalgorithm/usersubmission/">refresh</a>')

    def send_email(self, obj):
        return format_html('<a href="/admin/contact/?submittersname={0}&submittersemail={1}&name={2}" target="_blank">Send Email</a>'.format(obj.submittersname, obj.submittersemail, obj.name or ''))

    def Pfam(self, obj):
        return format_html()

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
        'name',
    )

    inlines = [ModelAdminLog]


# class ArchiveAdmin(admin.ModelAdmin):
#     search_fields = ('name', 'year', 'submittersname',
#                      'submittersemail')
#     fields = ('submittersname', 'submittersemail', 'name', 'year', 'sequence', 'bacterium', 'bacterium_textbox', 'taxonid', 'accession', 'partnerprotein', 'partnerprotein_textbox', 'toxicto', 'nontoxic', 'dnasequence', 'pdbcode', 'publication', 'comment', 'uploaded', 'predict_name', 'alignresults', 'terms_conditions')
#     list_display = ('name', 'submittersname',
#                      'accession', 'uploaded',)
#     ordering = ('-uploaded',)
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(UserSubmission, UserSubmissionAdmin)
admin.site.register(Archive, ArchiveAdmin)
admin.site.register(SendEmail, SendEmailAdmin)

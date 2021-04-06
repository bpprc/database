"""
This encapsulates the logic for displaying the models in the Django admin.




"""


from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import Group
from .models import PesticidalProteinDatabase, \
    Description, ProteinDetail, PesticidalProteinPrivateDatabase, OldnameNewnameTableLeft, OldnameNewnameTableRight, StructureDatabase, PesticidalProteinHiddenSequence
from import_export import resources
from django.utils.html import format_html
from django.db import models
from django.utils import timezone
from django.contrib.admin.checks import BaseModelAdminChecks
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.admin import GenericStackedInline
from django.contrib.admin.options import get_content_type_for_model

from django.forms import TextInput, Textarea
from Bio import Entrez

Entrez.email = 'sureshcbt@gmail.com'


# https://blog.askesis.pl/post/2019/02/django-admin-inline.html
class ModelAdminLog(GenericStackedInline):
    """
    A log message that stores the admin user, log in time, edited model class.
    """
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
        return obj.get_change_message()


class FilterByCategories(admin.SimpleListFilter):
    """
    A filter categories in the admin login to filter the data based on the category.
    """
    title = 'Categories'
    parameter_name = 'q'

    def lookups(self, request, model_admin):
        return [
            ('App', 'App'),
            ('Cry', 'Cry'),
            ('Cyt', 'Cyt'),
            ('Gpp', 'Gpp'),
            ('Mcf', 'Mcf'),
            ('Mpp', 'Mpp'),
            ('Mtx', 'Mtx'),
            ('Spp', 'Spp'),
            ('Tpp', 'Tpp'),
            ('Vip', 'Vip'),
            ('Vpa', 'Vpa'),
            ('Vpb', 'Vpb'),
            ('Xpp', 'Xpp'),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.distinct().filter()


class PesticidalProteinDatabaseResource(resources.ModelResource):
    """
    ModelResource is from django-import-export app and is a subclass
    for handling Django models.
    """
    class Meta:
        model = PesticidalProteinDatabase
        exclude = ('id', 'uploaded', 'fastasequence_file')


class PesticidalProteinPrivateDatabaseResource(resources.ModelResource):
    class Meta:
        model = PesticidalProteinPrivateDatabase


# https://stackoverflow.com/questions/45028975/django-import-export-cannot-exclude-id-field-during-import-keyerror-uid
class StructureDatabaseResource(resources.ModelResource):
    class Meta:
        model = StructureDatabase
        skip_unchanged = True
        report_skipped = True
        exclude = ('id',)
        import_id_fields = ('name', 'oldname', 'accession',
                            'pdbid', 'pubmedid', 'year', 'modified', 'comment')


class StructureDatabaseAdmin(ImportExportModelAdmin):
    resource_class = StructureDatabaseResource

    search_fields = ('name', 'oldname', 'accession',
                     'pdbid', 'pubmedid', 'year')
    fields = ('name', 'oldname', 'accession', 'pdbid',
              'modified', 'pubmedid', 'year', 'comment')
    list_display = ('name', 'oldname', 'accession', 'pdbid',
                    'modified', 'pubmedid', 'year', 'comment')
    ordering = ('name',)

    inlines = [ModelAdminLog]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:
            change_message = '{} - {} - {}'.format(
                obj.name, obj.oldname, obj.year, obj.accession, obj.pdbid, obj.modified, obj.pubmedid, obj.year, obj.comment)
            LogEntry.objects.create(
                user=request.user,
                content_type=get_content_type_for_model(obj),
                object_id=obj.id,
                action_flag=2,
                change_message=change_message,
                object_repr=obj.__str__()[:200]
            )


class PesticidalProteinPrivateDatabaseAdmin(ImportExportModelAdmin):
    resource_class = PesticidalProteinPrivateDatabaseResource
    # actions = None
    # actions = ['make_public']

    search_fields = ('name', 'oldname', 'othernames',
                     'accession', 'year', 'private')
    fields = ('name', 'oldname', 'othernames', 'accession', 'year',
              'sequence', 'uploaded', 'fastasequence_file', 'private', 'submittersname', 'submittersemail', 'bacterium', 'taxonid', 'bacterium_textbox', 'partnerprotein', 'partnerprotein_textbox', 'toxicto', 'nontoxic', 'dnasequence', 'publication', 'comment', 'admin_comments', 'created_by', 'created_on', 'edited_by', 'edited_on')
    list_display = ('name', 'oldname',
                    'accession_url', 'accession_availability', 'year', 'private')
    ordering = ('name',)

    inlines = [ModelAdminLog]

    def save_model(self, request, obj, form, change):
        user = request.user
        if user:
            obj.created_by = user
            obj.created_on = timezone.now()
            super().save_model(request, obj, form, change)
        super().save_model(request, obj, form, change)
        if change:
            obj.edited_by = request.user
            obj.edited_on = timezone.now()
            obj.save()
        if change:
            change_message = '{} - {} - {}'.format(
                obj.submittersname, obj.submittersemail, obj.name, obj.year, obj.sequence, obj.bacterium, obj.bacterium_textbox, obj.taxonid, obj.accession, obj.partnerprotein, obj.partnerprotein_textbox, obj.toxicto, obj.nontoxic, obj.dnasequence, obj.pdbcode, obj.publication, obj.comment, obj.predict_name)
            LogEntry.objects.create(
                user=request.user,
                content_type=get_content_type_for_model(obj),
                object_id=obj.id,
                action_flag=2,
                change_message=change_message,
                object_repr=obj.__str__()[:200]
            )

    def accession_url(self, obj):
        return format_html('<a href="%s%s" target="_blank">%s</a>' % ('https://www.ncbi.nlm.nih.gov/protein/', obj.accession, obj.accession))

    accession_url.allow_tags = True
    accession_url.description = 'View the accession number as an URL'

    def accession_availability(self, obj):
        accession = obj.accession
        if not accession:
            return format_html('<body> <p>No accession number</p> </body>')
        try:
            handle = Entrez.efetch(
                db="nucleotide", id=accession, rettype="fasta", retmode="text")
            return format_html('<body> <p style="color:#FF0000";>Sequence is Public</p> </body>')
        except:
            return format_html('<body> <p>Sequence is Private</p> </body>')

    accession_availability.allow_tags = True
    accession_availability.description = 'Accession Available in NCBI'

    # def get_changeform_initial_data(self, request):
    #     return {'admin_user': request.user.id}
    #
    # def make_public(self, request, queryset):
    #     queryset.update(public=True)


class PesticidalProteinHiddenSequenceAdmin(admin.ModelAdmin):
    # resource_class = PesticidalProteinHiddenSequence

    search_fields = ('name', 'othernames',
                     'accession', 'year', 'public')
    fields = ('name', 'othernames', 'accession', 'year', 'sequence', 'bacterium_textbox', 'strain',
              'publication', 'family', 'toxicto', 'nontoxic', 'mammalian_active', 'pdbcode', 'comment')
    list_display = ('name', 'othernames',
                    'accession', 'year', 'public')
    ordering = ('name',)

    inlines = [ModelAdminLog]

    def save_model(self, request, obj, form, change):
        user = request.user
        if user:
            obj.created_by = user
            obj.created_on = timezone.now()
            super().save_model(request, obj, form, change)
        super().save_model(request, obj, form, change)
        if change:
            obj.edited_by = request.user
            obj.edited_on = timezone.now()
            obj.save()
        if change:
            change_message = '{} - {} - {}'.format(
                obj.submittersname, obj.submittersemail, obj.name, obj.year, obj.sequence, obj.bacterium, obj.bacterium_textbox, obj.taxonid, obj.accession, obj.partnerprotein, obj.partnerprotein_textbox, obj.toxicto, obj.nontoxic, obj.dnasequence, obj.pdbcode, obj.publication, obj.comment, obj.predict_name)
            LogEntry.objects.create(
                user=request.user,
                content_type=get_content_type_for_model(obj),
                object_id=obj.id,
                action_flag=2,
                change_message=change_message,
                object_repr=obj.__str__()[:200]
            )


class PesticidalProteinDatabaseAdmin(ImportExportModelAdmin):
    resource_class = PesticidalProteinDatabaseResource
    # categories = PesticidalProteinDatabase.objects.order_by('name').values_list('name').distinct()
    search_fields = ('name', 'oldname',  'othernames',
                     'accession', 'year')
    fields = ('name', 'oldname',  'othernames', 'accession', 'year',
              'sequence', 'uploaded', 'fastasequence_file', 'public', 'pdbcode', 'submittersname', 'submittersemail', 'bacterium', 'taxonid', 'bacterium_textbox', 'partnerprotein', 'partnerprotein_textbox', 'toxicto', 'nontoxic', 'dnasequence', 'publication', 'comment', 'admin_comments', 'created_by', 'created_on', 'edited_by', 'edited_on')
    list_display = ('name', 'oldname',  'othernames',
                    'accession_url', 'year', 'public', 'Pfam_Info')
    list_filter = ['uploaded', FilterByCategories]
    ordering = ('name',)

    inlines = [ModelAdminLog]

    def save_model(self, request, obj, form, change):
        user = request.user
        if user:
            obj.created_by = user
            obj.created_on = timezone.now()
            super().save_model(request, obj, form, change)
        super().save_model(request, obj, form, change)
        if change:
            obj.edited_by = request.user
            obj.edited_on = timezone.now()
            obj.save()
        if change:
            change_message = '{} - {} - {}'.format(
                obj.submittersname, obj.submittersemail, obj.name, obj.year, obj.sequence, obj.bacterium, obj.bacterium_textbox, obj.taxonid, obj.accession, obj.partnerprotein, obj.partnerprotein_textbox, obj.toxicto, obj.nontoxic, obj.dnasequence, obj.pdbcode, obj.publication, obj.comment, obj.predict_name)
            LogEntry.objects.create(
                user=request.user,
                content_type=get_content_type_for_model(obj),
                object_id=obj.id,
                action_flag=2,
                change_message=change_message,
                object_repr=obj.__str__()[:200]
            )

    # def accession_url(self, obj):
    #     """Add URL to the accession number"""
    #     base_url = 'https://www.ncbi.nlm.nih.gov/protein/'
    #     return format_html('<a href="{url}" target="_blank">{url}</a>', url=base_url+obj.accession)
    def accession_url(self, obj):
        return format_html('<a href="%s%s" target="_blank">%s</a>' % ('https://www.ncbi.nlm.nih.gov/protein/', obj.accession, obj.accession))

    def Pfam_Info(self, obj):
        if obj.name.startswith('Cry'):
            try:
                domain_details = ProteinDetail.objects.get(
                    accession=obj.accession)
            except ProteinDetail.DoesNotExist:
                domain_details = None
            if domain_details:
                return format_html('<p>Data Available</p>')
            return format_html('<p style="color:#FF0000";>Pfam data needed</p>')

    accession_url.allow_tags = True
    accession_url.description = 'View the align results'


class DescriptionResource(resources.ModelResource):
    class Meta:
        model = Description


class DescriptionAdmin(ImportExportModelAdmin):
    resource_class = DescriptionResource
    fields = ('name', 'description')
    list_display = ('name', 'description')

    inlines = [ModelAdminLog]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:
            change_message = '{} - {} - {}'.format(
                obj.submittersname, obj.description)
            LogEntry.objects.create(
                user=request.user,
                content_type=get_content_type_for_model(obj),
                object_id=obj.id,
                action_flag=2,
                change_message=change_message,
                object_repr=obj.__str__()[:200]
            )


class OldnameNewnameTableLeftResource(resources.ModelResource):
    class Meta:
        model = OldnameNewnameTableLeft
        exclude = ('id')


class OldnameNewnameTableLeftAdmin(ImportExportModelAdmin):
    resource_class = OldnameNewnameTableLeftResource
    fields = ('name_2020', 'name_1998', 'alternative_name')
    list_display = ('name_2020', 'name_1998', 'alternative_name')

    inlines = [ModelAdminLog]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:
            change_message = '{} - {} - {}'.format(
                obj.name_2020, obj.name_1998, obj.alternative_name)
            LogEntry.objects.create(
                user=request.user,
                content_type=get_content_type_for_model(obj),
                object_id=obj.id,
                action_flag=2,
                change_message=change_message,
                object_repr=obj.__str__()[:200]
            )


class OldnameNewnameTableRightResource(resources.ModelResource):
    class Meta:
        model = OldnameNewnameTableRight
        exclude = ('id')


class OldnameNewnameTableRightAdmin(ImportExportModelAdmin):
    resource_class = OldnameNewnameTableRightResource
    fields = ('name_1998', 'name_2020', 'alternative_name')
    list_display = ('name_1998', 'name_2020', 'alternative_name')

    inlines = [ModelAdminLog]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:
            change_message = '{} - {} - {}'.format(
                obj.name_1998, obj.name_2020, obj.alternative_name)
            LogEntry.objects.create(
                user=request.user,
                content_type=get_content_type_for_model(obj),
                object_id=obj.id,
                action_flag=2,
                change_message=change_message,
                object_repr=obj.__str__()[:200]
            )


class ProteinDetailResource(resources.ModelResource):

    class Meta:
        model = ProteinDetail
        exclude = ('id', 'sequence')


class ProteinDetailAdmin(ImportExportModelAdmin):
    search_fields = ['name', 'accession', 'start_N', 'end_N',
                     'start_M', 'end_M', 'start_C', 'end_C']

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 80})}
    }
    fields = ('name', 'accession', 'fulllength', 'species', 'taxon', 'domain_N', 'pfam_N', 'cdd_N',
              'start_N', 'end_N', 'domain_M', 'pfam_M', 'cdd_M', 'start_M', 'end_M', 'domain_C', 'pfam_C', 'cdd_C', 'start_C', 'end_C')
    list_display = ('accession', 'Protein_Name', 'species', 'domain_N', 'pfam_N', 'cdd_N',
                    'start_N', 'end_N', 'domain_M', 'pfam_M', 'cdd_M', 'start_M', 'end_M', 'domain_C', 'pfam_C', 'cdd_C', 'start_C', 'end_C')
    ordering = ('accession',)

    inlines = [ModelAdminLog]

    def Protein_Name(self, obj):
        protein = PesticidalProteinDatabase.objects.get(
            accession=obj.accession)
        if protein:
            return protein.name

    class Meta:
        skip_unchanged = True
        report_skipped = True
        exclude = ('id', 'sequence')
        # import_id_fields = ('accession', 'fulllength', 'species', 'taxon', 'domain_N', 'pfam_N', 'cdd_N', 'start_N',
        #                     'end_N', 'domain_M', 'pfam_M', 'cdd_M', 'start_M', 'end_M', 'domain_C', 'pfam_C', 'cdd_C', 'start_C', 'end_C')


admin.site.site_header = 'BPPRC Admin Dashboard'
admin.site.index_title = 'BPPRC Available Features'
admin.site.site_title = 'BPPRC adminstration'

admin.site.register(PesticidalProteinDatabase, PesticidalProteinDatabaseAdmin)
admin.site.register(Description, DescriptionAdmin)
admin.site.register(ProteinDetail, ProteinDetailAdmin)
admin.site.register(PesticidalProteinPrivateDatabase,
                    PesticidalProteinPrivateDatabaseAdmin)
admin.site.register(PesticidalProteinHiddenSequence,
                    PesticidalProteinHiddenSequenceAdmin)
admin.site.register(StructureDatabase,
                    StructureDatabaseAdmin)
admin.site.register(OldnameNewnameTableLeft,
                    OldnameNewnameTableLeftAdmin)
admin.site.register(OldnameNewnameTableRight,
                    OldnameNewnameTableRightAdmin)
admin.site.unregister(Group)

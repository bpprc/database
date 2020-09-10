"""
This encapsulates the logic for displaying the models in the Django admin.




"""


from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import Group
from .models import PesticidalProteinDatabase, \
    Description, ProteinDetail, PesticidalProteinPrivateDatabase, PesticidalProteinStructureDatabase, OldnameNewnameTableLeft, OldnameNewnameTableRight
from import_export import resources
from django.db import models
from django.forms import TextInput, Textarea


class FilterByCategories(admin.SimpleListFilter):
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
    class Meta:
        model = PesticidalProteinDatabase
        exclude = ('id', 'uploaded', 'fastasequence_file')


class PesticidalProteinPrivateDatabaseResource(resources.ModelResource):
    class Meta:
        model = PesticidalProteinPrivateDatabase


class PesticidalProteinStructureDatabaseResource(resources.ModelResource):
    class Meta:
        model = PesticidalProteinStructureDatabase


class PesticidalProteinStructureDatabaseAdmin(ImportExportModelAdmin):
    resource_class = PesticidalProteinStructureDatabaseResource

    search_fields = ('name', 'accession', 'uniprot', 'gene_names', 'pdbid', 'pubmedid', 'year', 'chimeric', 'organism', 'expression_system',
                     'length', 'resolution', 'experiment_method', 'release_date', 'deposited', 'publication', 'structure_file', 'structure_doi')
    fields = ('name', 'uniprot', 'gene_names', 'pdbid',
              'pubmedid', 'year', 'chimeric', 'organism', 'length', 'resolution', 'expression_system', 'experiment_method', 'release_date', 'deposited', 'publication', 'structure_file', 'structure_doi')
    list_display = ('name', 'accession', 'uniprot', 'gene_names', 'pdbid',
                    'pubmedid', 'year', 'chimeric', 'organism', 'expression_system', 'length', 'resolution', 'experiment_method', 'structure_file', 'structure_doi')
    ordering = ('name',)


class PesticidalProteinPrivateDatabaseAdmin(admin.ModelAdmin):
    # resource_class = PesticidalProteinPrivateDatabaseResource
    # actions = None
    actions = ['make_public']

    search_fields = ('name', 'oldname', 'othernames',
                     'accession', 'year', 'private')
    fields = ('name', 'oldname', 'othernames', 'accession', 'year',
              'sequence', 'uploaded', 'fastasequence_file', 'private', 'admin_user')
    list_display = ('name', 'oldname',  'othernames',
                    'accession', 'year', 'fastasequence_file', 'private')
    ordering = ('name',)

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def get_changeform_initial_data(self, request):
        return {'admin_user': request.user.id}

    def make_public(self, request, queryset):
        queryset.update(public=True)

    # def has_change_permission(self, request, obj=None):
    #     return False
    # def move_to_public(self, request):
    # save_on_top = True


class PesticidalProteinDatabaseAdmin(ImportExportModelAdmin):
    resource_class = PesticidalProteinDatabaseResource
    # categories = PesticidalProteinDatabase.objects.order_by('name').values_list('name').distinct()
    search_fields = ('name', 'oldname',  'othernames',
                     'accession', 'year', 'public', 'pdbcode')
    fields = ('name', 'oldname',  'othernames', 'accession', 'year',
              'sequence', 'uploaded', 'fastasequence_file', 'public', 'pdbcode')
    list_display = ('name', 'oldname',  'othernames',
                    'accession', 'year', 'public', 'pdbcode')
    list_filter = ['uploaded', FilterByCategories]
    ordering = ('name',)


class DescriptionResource(resources.ModelResource):
    class Meta:
        model = Description


class DescriptionAdmin(ImportExportModelAdmin):
    resource_class = DescriptionResource
    fields = ('name', 'description')
    list_display = ('name', 'description')


class OldnameNewnameTableLeftResource(resources.ModelResource):
    class Meta:
        model = OldnameNewnameTableLeft
        exclude = ('id')


class OldnameNewnameTableLeftAdmin(ImportExportModelAdmin):
    resource_class = OldnameNewnameTableLeftResource
    fields = ('name_2020', 'name_1998', 'alternative_name')
    list_display = ('name_2020', 'name_1998', 'alternative_name')


class OldnameNewnameTableRightResource(resources.ModelResource):
    class Meta:
        model = OldnameNewnameTableRight
        exclude = ('id')


class OldnameNewnameTableRightAdmin(ImportExportModelAdmin):
    resource_class = OldnameNewnameTableRightResource
    fields = ('name_1998', 'name_2020', 'alternative_name')
    list_display = ('name_1998', 'name_2020', 'alternative_name')


class ProteinDetailResource(resources.ModelResource):

    class Meta:
        model = ProteinDetail
        exclude = ('id', 'sequence')


class ProteinDetailAdmin(ImportExportModelAdmin):
    search_fields = ['accession', 'start_N', 'end_N',
                     'start_M', 'end_M', 'start_C', 'end_C']

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 80})}
    }
    fields = ('accession', 'fulllength', 'species', 'taxon', 'domain_N', 'pfam_N', 'cdd_N',
              'start_N', 'end_N', 'domain_M', 'pfam_M', 'cdd_M', 'start_M', 'end_M', 'domain_C', 'pfam_C', 'cdd_C', 'start_C', 'end_C')
    list_display = ('accession', 'fulllength', 'species', 'taxon', 'domain_N', 'pfam_N', 'cdd_N',
                    'start_N', 'end_N', 'domain_M', 'pfam_M', 'cdd_M', 'start_M', 'end_M', 'domain_C', 'pfam_C', 'cdd_C', 'start_C', 'end_C')

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
admin.site.register(PesticidalProteinStructureDatabase,
                    PesticidalProteinStructureDatabaseAdmin)
admin.site.register(OldnameNewnameTableLeft,
                    OldnameNewnameTableLeftAdmin)
admin.site.register(OldnameNewnameTableRight,
                    OldnameNewnameTableRightAdmin)
admin.site.unregister(Group)

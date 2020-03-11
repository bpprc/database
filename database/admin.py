from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import Group
from .models import PesticidalProteinDatabase, \
    Description, ProteinDetail, PesticidalProteinPrivateDatabase
from import_export import resources
from django.db import models
from django.forms import TextInput, Textarea

# allmat = [c.name for c in PesticidalProteinDatabase.objects.all()]  # fetch the names from the model
# mat = [c[0:3] for c in allmat] # fetch the first three letter pattern from the list of names
# myset = set(mat) #Keep unique names in the list


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


class PesticidalProteinPrivateDatabaseAdmin(ImportExportModelAdmin):
    resource_class = PesticidalProteinPrivateDatabaseResource

    search_fields = ('name', 'oldname', 'othernames', 'accession', 'year')
    fields = ('name', 'oldname', 'othernames', 'accession', 'year',
              'sequence', 'uploaded')
    list_display = ('name', 'oldname',  'othernames', 'accession', 'year',)
    ordering = ('name',)


class PesticidalProteinDatabaseAdmin(ImportExportModelAdmin):
    resource_class = PesticidalProteinDatabaseResource
    # categories = PesticidalProteinDatabase.objects.order_by('name').values_list('name').distinct()
    search_fields = ('name', 'oldname',  'othernames', 'accession', 'year')
    fields = ('name', 'oldname',  'othernames', 'accession', 'year',
              'sequence', 'uploaded', 'fastasequence_file')
    list_display = ('name', 'oldname',  'othernames', 'accession', 'year',)
    list_filter = ['uploaded', FilterByCategories]
    ordering = ('name',)


class DescriptionResource(resources.ModelResource):
    class Meta:
        model = Description


class DescriptionAdmin(ImportExportModelAdmin):
    resource_class = DescriptionResource
    fields = ('name', 'description')
    list_display = ('name', 'description')


class ProteinDetailAdmin(admin.ModelAdmin):
    search_fields = ['accession']

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 80})}
    }
    fields = ('accession', 'fulllength', 'species', 'taxon', 'domain_N', 'pfam_N', 'cdd_N',
              'start_N', 'end_N', 'domain_M', 'pfam_M', 'cdd_M', 'start_M', 'end_M', 'domain_C', 'pfam_C', 'cdd_C', 'start_C', 'end_C')
    list_display = ('accession', 'fulllength', 'species', 'taxon', 'domain_N', 'pfam_N', 'cdd_N',
                    'start_N', 'end_N', 'domain_M', 'pfam_M', 'cdd_M', 'start_M', 'end_M', 'domain_C', 'pfam_C', 'cdd_C', 'start_C', 'end_C')


admin.site.site_header = 'BPPRC Admin Dashboard'
admin.site.index_title = 'BPPRC Available Features'
admin.site.site_title = 'BPPRC adminstration'

admin.site.register(PesticidalProteinDatabase, PesticidalProteinDatabaseAdmin)
admin.site.register(Description, DescriptionAdmin)
admin.site.register(ProteinDetail, ProteinDetailAdmin)
admin.site.register(PesticidalProteinPrivateDatabase,
                    PesticidalProteinPrivateDatabaseAdmin)
admin.site.unregister(Group)

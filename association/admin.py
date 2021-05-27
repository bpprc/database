from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Association


class AssociationResource(resources.ModelResource):
    class Meta:
        model = Association
        exclude = ("id",)
        import_id_fields = (
            "name",
            "partnerprotein",
            "partnerprotein_textbox",
            "target_order",
            "target_species",
            "activity",
            "taxonid",
            "lc50",
            "units",
            "percentage_mortality",
            "publication",
            "other_citations",
            "life_stage",
            "instar",
            "assay_material",
            "assay_method",
            "comment",
            "data_entered_by",
        )


class AssociationAdmin(ImportExportModelAdmin):
    resource_class = AssociationResource

    search_fields = (
        "name",
        "partnerprotein",
        "partnerprotein_textbox",
        "target_order",
        "target_species",
        "activity",
        "taxonid",
        "lc50",
        "units",
        "percentage_mortality",
        "publication",
        "other_citations",
        "life_stage",
        "instar",
        "assay_material",
        "assay_method",
        "data_entered_by",
    )

    fields = (
        "name",
        "partnerprotein",
        "partnerprotein_textbox",
        "target_order",
        "target_species",
        "activity",
        "taxonid",
        "lc50",
        "units",
        "percentage_mortality",
        "publication",
        "other_citations",
        "life_stage",
        "instar",
        "assay_material",
        "assay_method",
        "comment",
        "data_entered_by",
    )

    list_display = (
        "name",
        "partnerprotein",
        "partnerprotein_textbox",
        "target_order",
        "target_species",
        "activity",
        "taxonid",
        "lc50",
        "units",
        "percentage_mortality",
        "publication",
        "other_citations",
        "life_stage",
        "instar",
        "assay_material",
        "assay_method",
        "comment",
        "data_entered_by",
    )


admin.site.register(Association, AssociationAdmin)

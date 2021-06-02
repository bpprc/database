from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from extra.models import Feedback, Links

# Register your models here.


class LinksResource(resources.ModelResource):
    class Meta:
        model = Links


class LinksAdmin(ImportExportModelAdmin):
    resource_class = LinksResource

    list_display = ("name", "description", "link_url")

    def __str__(self):
        return self.name

    def link_url(self, obj):
        return format_html('<a href="%s" target="_blank">%s</a>' % (obj.link, obj.link))


class FeedbackResource(resources.ModelResource):
    class Meta:
        model = Feedback


class FeedbackAdmin(ImportExportModelAdmin):
    resource_class = FeedbackResource
    list_editable = ("contact_status",)
    list_display = ("name", "subject", "email", "uploaded", "contact_status",)

    # def save_model(self, request, obj, form, change):
    #     obj.user = request.user
    #     super().save_model(request, obj, form, change)

    def __str__(self):
        return self.name


admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Links, LinksAdmin)

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from extra.models import Feedback, Links

# Register your models here.


class LinksResource(resources.ModelResource):

    class Meta:
        model = Links


class LinksAdmin(ImportExportModelAdmin):
    resource_class = LinksResource

    list_display = ('name', 'description', 'link',)

    def __str__(self):
        return self.name


class FeedbackResource(resources.ModelResource):

    class Meta:
        model = Feedback


class FeedbackAdmin(ImportExportModelAdmin):
    resource_class = FeedbackResource

    list_display = ('name', 'subject', 'email')

    def __str__(self):
        return self.name


admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Links, LinksAdmin)

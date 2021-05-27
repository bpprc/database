from django.contrib import admin

from clustalanalysis.models import StoreResultFiles


class StoreResultFilesAdmin(admin.ModelAdmin):
    fields = ["taskid", "tempfile", "resultfile"]


admin.site.register(StoreResultFiles, StoreResultFilesAdmin)

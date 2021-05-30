from django.core.files.base import ContentFile
from django.db import models


class StoreResultFiles(models.Model):
    taskid = models.CharField(max_length=250, blank=True, null=False)
    tempfile = models.CharField(max_length=1000, null=True)
    resultfile = models.FileField(
        upload_to="store_result_files/", null=True, blank=True)
    # newlines = models.CharField(max_length=100, blank=True)
    # radius = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        is_create = not bool(self.id)
        super().save(*args, **kwargs)
        if is_create:
            with open(self.tempfile, "r") as content_file:
                result = content_file.read()
                filename = "id_{}".format(self.id)
                content = ContentFile(result)
                self.resultfile.save(filename, content)
                # super(StoreResultFiles, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Store result file"
        verbose_name_plural = "Store results files"

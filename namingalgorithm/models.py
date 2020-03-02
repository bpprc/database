from django.db import models
from django.contrib import admin
from django.utils import timezone


class UserSubmission(models.Model):
    name = models.CharField(max_length=25, null=True, blank=True)
    year = models.CharField(max_length=4, null=True, blank=True)
    fastasequence = models.TextField(null=True, blank=False)
    comment = models.TextField(null=True, blank=True)
    email = models.EmailField(max_length=70, null=True, blank=False)
    uploaded = models.DateTimeField('Uploaded', default=timezone.now)
    alignresults = models.TextField(null=True, blank=True)
    predict_name = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('email',)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name

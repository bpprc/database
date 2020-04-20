from django.db import models
from django.contrib import admin
from django.utils import timezone

TRUE_FALSE_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)


class BacteriaTaxonID(models.Model):
    taxonid = models.CharField(max_length=250, null=True, blank=True)
    bacterianame = models.TextField(null=True, blank=False)


class UserSubmission(models.Model):

    submittersname = models.CharField(max_length=25, null=True, blank=True)
    submittersemail = models.EmailField(max_length=70, null=True, blank=False)
    proteinsname = models.CharField(max_length=25, null=True, blank=True)
    proteinsequence = models.TextField(null=True, blank=False)
    bacterium = models.BooleanField(default=True, choices=TRUE_FALSE_CHOICES)
    bacterium_textbox = models.CharField(
        max_length=250, null=True, blank=True)
    # sourcebacterium = models.BooleanField(
    #     default=True, choices=TRUE_FALSE_CHOICES)
    # sourcebacterium_textbox = models.CharField(
    #     max_length=250, null=True, blank=True)
    taxonid = models.CharField(max_length=25, null=True, blank=True)
    year = models.CharField(max_length=4, null=True, blank=True)
    accessionnumber = models.CharField(max_length=25, blank=True, null=False)
    partnerprotein = models.BooleanField(
        default=True, choices=TRUE_FALSE_CHOICES)
    partnerprotein_textbox = models.CharField(
        max_length=250, null=True, blank=True)
    toxicto = models.CharField(max_length=250, blank=True, null=False)
    nontoxic = models.CharField(max_length=250, blank=True, null=False)
    dnasequence = models.TextField(null=True, blank=False)
    pdbcode = models.CharField(max_length=10, blank=True, null=False)
    publication = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    uploaded = models.DateTimeField('Uploaded', default=timezone.now)
    alignresults = models.TextField(null=True, blank=True)
    predict_name = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('submittersemail',)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

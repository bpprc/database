from django.db import models


TRUE_FALSE_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)


class DataModel(models.Model):
    name = models.CharField(max_length=25,
                            blank=True, verbose_name="Protein Name")
    accession = models.CharField(
        max_length=25, blank=True, null=False, verbose_name="NCBI accession number")
    partnerprotein = models.BooleanField(
        default=True, choices=TRUE_FALSE_CHOICES)
    partnerprotein_textbox = models.CharField(
        max_length=250, blank=True)
    target_order = models.CharField(
        max_length=250, blank=True)
    target_species = models.CharField(
        max_length=250, null=True, blank=True)
    activity = models.BooleanField(
        default=True, choices=TRUE_FALSE_CHOICES)
    taxonid = models.CharField(max_length=25, blank=True)
    lc50 = models.CharField(max_length=25, blank=True)
    units = models.CharField(max_length=25, blank=True)
    percentage_mortality = models.CharField(max_length=25, blank=True)
    publication = models.TextField(blank=True)
    stage = models.CharField(max_length=75, blank=True)
    assay_material = models.TextField(blank=True)
    assay_method = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    data_entered_by = models.CharField(
        max_length=250, null=True, blank=True)

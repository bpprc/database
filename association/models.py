from django.db import models


TRUE_FALSE_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)


class Association(models.Model):
    name = models.TextField(blank=True, verbose_name="Protein Name")
    oldname = models.TextField(blank=True, verbose_name="Old Name")
    accession = models.TextField(
        blank=True, verbose_name="NCBI accession number")
    partnerprotein = models.CharField(max_length=7,
                                      default='No', editable=True)
    partnerprotein_textbox = models.TextField(blank=True)
    target_order = models.TextField(blank=True)
    target_species = models.TextField(null=True, blank=True)
    activity = models.CharField(max_length=7,
                                default='Yes', editable=True)
    taxonid = models.TextField(blank=True)
    lc50 = models.TextField(blank=True)
    units = models.TextField(blank=True)
    # non_toxic = models.TextField(blank=True)
    percentage_mortality = models.TextField(blank=True)
    publication = models.TextField(blank=True)
    other_citations = models.TextField(blank=True)
    life_stage = models.TextField(blank=True)
    instar = models.TextField(blank=True)
    assay_material = models.TextField(blank=True)
    assay_method = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    data_entered_by = models.TextField(blank=True)

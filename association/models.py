from django.db import models

TRUE_FALSE_CHOICES = ((True, "Yes"), (False, "No"))


# class KeywordDatabase(models.Model):
#
#     keyword_id = models.AutoField(primary_key=True)
#
#     def get_database_name_as_list(self):
#         return ', '.join(self.Association_set.values_list('name', flat=True))
#
#     def get_database_target_species_as_list(self):
#         return ', '.join(self.Association_set.values_list('target_species', flat=True))
#
#     def get_database_target_order_as_list(self):
#         return ', '.join(self.Association_set.values_list('target_order', flat=True))
#
#     def get_database_taxonid_as_list(self):
#         return ', '.join(self.Association_set.values_list('taxonid', flat=True))


class Association(models.Model):
    name = models.TextField(blank=True, verbose_name="Protein Name")
    # oldname = models.TextField(blank=True, verbose_name="Old Name")
    # accession = models.TextField(
    #     blank=True, verbose_name="NCBI accession number")
    partnerprotein = models.CharField(
        max_length=255, default="No", editable=True
    )
    partnerprotein_textbox = models.TextField(
        blank=True, default="No", editable=True
    )
    target_order = models.TextField(null=True)
    target_species = models.TextField(null=True)
    activity = models.CharField(
        max_length=7, default="Yes", editable=True
    )
    taxonid = models.TextField(null=True)
    lc50 = models.TextField(null=True)
    units = models.TextField(null=True)
    non_toxic = models.TextField(null=True)
    percentage_mortality = models.TextField(null=True)
    publication = models.TextField(null=True)
    other_citations = models.TextField(null=True)
    life_stage = models.TextField(null=True)
    instar = models.TextField(null=True)
    assay_material = models.TextField(null=True)
    assay_method = models.TextField(null=True)
    comment = models.TextField(null=True)
    data_entered_by = models.TextField(null=True)
    # keywords_data = models.ForeignKey(
    #     'KeywordDatabase', on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return self.name

    def get_target_order(self):
        return self.target_order

    def get_target_species(self):
        return self.target_species

    # def get_database_target_species_as_list(self):
    #     return ', '.join(self.Association.values('target_species', flat=True))
    #
    # def get_database_target_order_as_list(self):
    #     return self.target_order
    #
    # def get_database_taxonid_as_list(self):
    #     return ', '.join(self.Association.values('taxonid', flat=True))
    #
    # def get_target_order(self):
    #     return json.loads(self.target_order)

    class Meta:
        verbose_name = "Association data"

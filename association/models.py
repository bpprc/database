from django.db import models


TRUE_FALSE_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)


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
    non_toxic = models.TextField(blank=True)
    percentage_mortality = models.TextField(blank=True)
    publication = models.TextField(blank=True)
    other_citations = models.TextField(blank=True)
    life_stage = models.TextField(blank=True)
    instar = models.TextField(blank=True)
    assay_material = models.TextField(blank=True)
    assay_method = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    data_entered_by = models.TextField(blank=True)
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
        verbose_name = 'Association data'

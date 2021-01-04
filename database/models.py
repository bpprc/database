""" """

import re
import textwrap
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from django.db import models
from django.utils import timezone
from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.utils.html import format_html


TRUE_FALSE_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)


class OldnameNewnameTableLeft(models.Model):
    name_2020 = models.CharField(max_length=250, blank=True, null=False)
    name_1998 = models.CharField(max_length=250, blank=True, null=False)
    alternative_name = models.CharField(max_length=250, blank=True, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ("Organized by new name")
        verbose_name_plural = "Organized by new name"


class OldnameNewnameTableRight(models.Model):
    name_1998 = models.CharField(max_length=250, blank=True, null=False)
    name_2020 = models.CharField(max_length=250, blank=True, null=False)
    alternative_name = models.CharField(max_length=250, blank=True, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ("Organized by Oldname")
        verbose_name_plural = "Organized by Oldname"


CHOICES = [
    ('yes', 'Yes'),
    ('no', 'No'),
]


class StructureDatabase(models.Model):
    name = models.CharField(max_length=25, blank=True, null=False)
    oldname = models.CharField(max_length=75, blank=True, null=False)
    accession = models.CharField(max_length=75, blank=True, null=False)
    #uniprot = models.CharField(max_length=25, blank=True, null=False)
    #pdbid = models.JSONField(max_length=500, blank=True, null=False)
    pdbid = ArrayField(models.CharField(
        max_length=1000, blank=True), default=list)
    #ligand = models.CharField(max_length=250, blank=True, null=False)
    #gene_names = models.CharField(max_length=250, blank=True, null=False)
    #experiment_method = models.CharField(max_length=250, blank=True, null=False)
    #resolution = models.CharField(max_length=250, blank=True, null=False)
    #deposited = models.DateTimeField('deposition date', default=timezone.now)
    #release_date = models.DateTimeField('release date', default=timezone.now)
    #publication = models.TextField(blank=True, null=False)
    pubmedid = models.CharField(max_length=75, blank=True, null=False)
    year = models.CharField(max_length=5, blank=True, null=False)
    modified = models.CharField(max_length=100, choices=CHOICES, default="Yes")
    comment = models.TextField(null=True, blank=True)
    #organism = models.CharField(max_length=250, blank=True)
    #expression_system = models.CharField(max_length=250, blank=True)
    #length = models.CharField(max_length=25, blank=True, null=False)
    #structure_file = models.FileField(upload_to='pdb_files/', null=True, blank=True)
    #structure_doi = models.CharField(max_length=250, blank=True, null=False)
    #bt = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Structure Information'
        verbose_name_plural = "Structure Database"


class PesticidalProteinHiddenSequence(models.Model):
    """
    """
    name = models.CharField(max_length=15, default="None")
    oldname = models.CharField(max_length=305, default="None")
    othernames = models.TextField(blank=True, null=False)
    accession = models.CharField(max_length=25)
    year = models.CharField(max_length=5, default="None")
    sequence = models.TextField(blank=True, null=False)
    bacterium = models.BooleanField(default=True, choices=TRUE_FALSE_CHOICES)
    bacterium_textbox = models.CharField(
        max_length=250, default="Bacillus Thuringiensis")
    strain = models.CharField(
        max_length=250, default="None")
    publication = models.TextField(null=True, blank=True)
    family = models.CharField(max_length=305, blank=True, default="None")
    toxicto = models.CharField(max_length=250, blank=True, default="None")
    nontoxic = models.CharField(max_length=250, blank=True, default="None")
    mammalian_active = models.CharField(
        max_length=250, blank=True, default="None")
    pdbcode = models.CharField(max_length=10, blank=True, default="None")
    comment = models.TextField(null=True, blank=True)
    submittersname = models.CharField(max_length=25, default="None")
    submittersemail = models.EmailField(max_length=70, default="None")
    taxonid = models.CharField(max_length=25, default="None")
    partnerprotein = models.BooleanField(
        default=True, choices=TRUE_FALSE_CHOICES)
    partnerprotein_textbox = models.CharField(
        max_length=250, default="None")
    dnasequence = models.TextField(null=True, blank=False)
    uploaded = models.DateTimeField('Uploaded', default=timezone.now)
    alignresults = models.TextField(null=True, blank=True)
    predict_name = models.TextField(null=True, blank=True)
    terms_conditions = models.BooleanField(
        default=False, choices=TRUE_FALSE_CHOICES)
    admin_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE, null=True, blank=True)
    admin_comments = models.TextField(null=True, blank=True)
    public = models.BooleanField(default=False)
    private = models.BooleanField(default=True, choices=TRUE_FALSE_CHOICES)
    oldname = models.CharField(max_length=105, blank=True, null=False)
    othernames = models.TextField(blank=True, null=False)
    fastasequence_file = models.FileField(
        upload_to='fastasequence_files/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Hidden sequence'
        verbose_name_plural = "Hidden sequences for naming purpose"


class PesticidalProteinPrivateDatabase(models.Model):
    """
    """
    submittersname = models.CharField(max_length=25, null=True, blank=True)
    submittersemail = models.EmailField(max_length=70, null=True, blank=False)
    name = models.CharField(max_length=15, blank=True,
                            null=False, verbose_name="Protein Name")
    sequence = models.TextField(
        blank=True, null=False, verbose_name="Protein Sequence")
    bacterium = models.BooleanField(default=True, choices=TRUE_FALSE_CHOICES)
    bacterium_textbox = models.CharField(
        max_length=250, null=True, blank=True)
    taxonid = models.CharField(max_length=25, null=True, blank=True)
    year = models.CharField(max_length=5, blank=True, null=False)
    accession = models.CharField(
        max_length=25, blank=True, null=False, verbose_name="NCBI accession number")
    partnerprotein = models.BooleanField(
        default=True, choices=TRUE_FALSE_CHOICES)
    partnerprotein_textbox = models.CharField(
        max_length=250, null=True, blank=True)
    toxicto = models.CharField(max_length=250, blank=True, null=False)
    nontoxic = models.CharField(max_length=250, blank=True, null=False)
    dnasequence = models.TextField(null=True, blank=False)
    pdbcode = models.CharField(max_length=10, blank=True, null=False)
    publication = models.TextField(null=True, blank=True)
    comment = models.TextField(
        null=True, blank=True, verbose_name="User comments")
    uploaded = models.DateTimeField('Uploaded', default=timezone.now)
    alignresults = models.TextField(null=True, blank=True)
    predict_name = models.TextField(null=True, blank=True)
    terms_conditions = models.BooleanField(
        default=False, choices=TRUE_FALSE_CHOICES)
    admin_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE, null=True, blank=True)
    admin_comments = models.TextField(null=True, blank=True)
    public = models.BooleanField(default=False)
    private = models.BooleanField(default=True, choices=TRUE_FALSE_CHOICES)
    oldname = models.CharField(max_length=105, blank=True, null=False)
    othernames = models.TextField(blank=True, null=False)
    fastasequence_file = models.FileField(
        upload_to='fastasequence_files/', null=True, blank=True)
    name_category = models.CharField(max_length=15, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_created_by", null=True, blank=True)
    created_on = models.DateTimeField(
        'Created on', null=True, blank=True, default=timezone.now)
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="%(class)s_edited_by")
    edited_on = models.DateTimeField(
        'Edited on', null=True, blank=True, default=timezone.now)
    # published = models.BooleanField(default=True, choices=TRUE_FALSE_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Private Sequence'
        verbose_name_plural = "Private Sequences"


class PesticidalProteinDatabase(models.Model):
    """
    """
    submittersname = models.CharField(
        max_length=125, blank=True, default="Uploaded by Suresh")
    submittersemail = models.EmailField(
        max_length=70, blank=True)
    name = models.CharField(max_length=15, blank=True,
                            null=False, verbose_name="Protein Name")
    oldname = models.CharField(max_length=105, blank=True, null=False)
    othernames = models.TextField(blank=True, null=False)
    accession = models.CharField(
        max_length=25, blank=True, null=False, verbose_name="NCBI accession number")
    year = models.CharField(max_length=5, blank=True, null=False)
    sequence = models.TextField(
        blank=True, null=False, verbose_name="Protein Sequence")
    bacterium = models.BooleanField(default=True, choices=TRUE_FALSE_CHOICES)
    taxonid = models.CharField(max_length=25, null=True, blank=True)
    bacterium_textbox = models.CharField(
        max_length=250, null=True, blank=True)
    partnerprotein = models.BooleanField(
        default=True, choices=TRUE_FALSE_CHOICES)
    partnerprotein_textbox = models.CharField(
        max_length=250, null=True, blank=True)
    toxicto = models.CharField(max_length=250, blank=True, null=False)
    nontoxic = models.CharField(max_length=250, blank=True, null=False)
    dnasequence = models.TextField(blank=True)
    publication = models.TextField(null=True, blank=True)
    comment = models.TextField(
        null=True, blank=True, verbose_name="User comments")
    uploaded = models.DateTimeField('Uploaded', default=timezone.now)
    fastasequence_file = models.FileField(
        upload_to='fastasequence_files/', null=True, blank=True)
    name_category = models.CharField(max_length=15, blank=True)
    public = models.BooleanField(default=True)
    pdbcode = models.CharField(max_length=10, blank=True, null=False)
    predict_name = models.TextField(null=True, blank=True)
    terms_conditions = models.BooleanField(
        default=False, choices=TRUE_FALSE_CHOICES)
    admin_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE, null=True, blank=True)
    admin_comments = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_created_by", null=True, blank=True,)
    created_on = models.DateTimeField(
        'Created on', null=True, blank=True, default=timezone.now)
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="%(class)s_edited_by")
    edited_on = models.DateTimeField(
        'Edited on', null=True, blank=True, default=timezone.now)
    published = models.BooleanField(default=False, choices=TRUE_FALSE_CHOICES)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Public Sequence'
        verbose_name_plural = "Public Sequences"

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name_category = re.search(
            r"[A-Z][a-z]{2}\d{1,3}", self.name).group()
        self.oldname_category = re.search(
            r"[A-Z][a-z]{2}\d{1,3}", self.name).group()
        # TODO clear out old file before saving new one?
        filename = 'fasta{}'.format(self.name)
        file_contents = '>{}\n{}\n'.format(self.name, self.sequence)
        # print(file_contents)
        content = ContentFile(file_contents)
        self.fastasequence_file.save(filename, content, save=False)
        super().save(*args, **kwargs)

    def category_name(self):
        return self.name[0][:3]

    def get_fastasequence(self):
        fasta = textwrap.fill(str(self.sequence), 80)
        str_to_write = f"{self.name}\n{fasta}\n"
        return str_to_write

    def get_sequence_length(self):
        return len(self.sequence)

    def get_sequence_aromaticity(self):
        x = ProteinAnalysis(self.sequence)
        return "{0:0.2f}".format(x.aromaticity())

    def get_sequence_molecular_weight(self):
        x = ProteinAnalysis(self.sequence)
        x = x.molecular_weight() / 1000
        #x = x.molecular_weight()
        # return "{0:0.2f}".format(x.molecular_weight())
        return "{0:0.2f}".format(x)

    def get_sequence_instability_index(self):
        x = ProteinAnalysis(self.sequence)
        return "{0:0.2f}".format(x.instability_index())

    def get_sequence_isoelectric_point(self):
        x = ProteinAnalysis(self.sequence)
        return "{0:0.2f}".format(x.isoelectric_point())

    def get_sequence_count_aminoacids(self):
        x = ProteinAnalysis(self.sequence)
        return x.count_amino_acids()  # how to draw histogram

    def get_sequence_get_amino_acids_percent(self):
        x = ProteinAnalysis(self.sequence)
        return x.get_amino_acids_percent()

    def get_secondary_structure(self):
        x = ProteinAnalysis(self.sequence)
        sec_stru = x.secondary_structure_fraction()
        helix = "{0:0.2f}".format(sec_stru[0])
        turn = "{0:0.2f}".format(sec_stru[1])
        sheet = "{0:0.2f}".format(sec_stru[2])
        return helix, turn, sheet

    # def Pfam_Info(self):
    #     if self.name.startswith('Cry'):
    #         domain_details = ProteinDetail.objects.get(accession=self.accession)
    #         print(domain_details)
    #         if not domain_details:
    #             return format_html('<body> <p style="color:#FF0000";>Pfam data needed</p> </body>')
    #         else:
    #             return format_html('Data Available')
    #
    # else:
    #     return format_html('Data Available')


# class BacteriaTaxonomy(models.Model):
#     bacteria_name = models.CharField(max_length=100, blank=False)
#     bacteria_taxonid = models.IntegerField(max_length=20, blank=False)

class ProteinDetail(models.Model):

    # name = models.ForeignKey(PesticidalProteinDatabase, related_name="%(class)s_name", on_delete=models.CASCADE,)
    # accession = models.ForeignKey(PesticidalProteinDatabase, related_name="%(class)s_accession", on_delete=models.CASCADE,)
    # sequence = models.ForeignKey(PesticidalProteinDatabase, related_name="%(class)s_fastasequence", on_delete=models.CASCADE,)
    accession = models.CharField(max_length=25, blank=True, null=False)
    sequence = models.TextField(blank=True, null=False)
    fulllength = models.TextField(blank=True, null=False)
    species = models.TextField(blank=True, null=False)
    taxon = models.TextField(blank=True, null=False)
    domain_N = models.TextField(blank=True, null=False)
    pfam_N = models.CharField(max_length=25, blank=True, null=False)
    cdd_N = models.CharField(max_length=25, blank=True, null=False)
    start_N = models.CharField(max_length=10, blank=True, null=False)
    end_N = models.CharField(max_length=10, blank=True, null=False)
    domain_M = models.TextField(blank=True, null=False)
    pfam_M = models.CharField(max_length=25, blank=True, null=False)
    cdd_M = models.CharField(max_length=25, blank=True, null=False)
    start_M = models.CharField(max_length=10, blank=True, null=False)
    end_M = models.CharField(max_length=10, blank=True, null=False)
    domain_C = models.TextField(blank=True, null=False)
    pfam_C = models.CharField(max_length=25, blank=True, null=False)
    cdd_C = models.CharField(max_length=10, blank=True, null=False)
    start_C = models.CharField(max_length=10, blank=True, null=False)
    end_C = models.CharField(max_length=10, blank=True, null=False)

    class Meta:
        verbose_name_plural = "Three domains data"

    def get_endotoxin_n(self):
        if not self.start_N or not self.end_N:
            return ''
        sequence = self.sequence
        return sequence[int(self.start_N):int(self.end_N)]

    def get_endotoxin_m(self):
        if not self.start_M or not self.end_M:
            return ''
        sequence = self.sequence
        return sequence[int(self.start_M):int(self.end_M)]

    def get_endotoxin_c(self):
        if not self.start_C or not self.end_C:
            return ''
        sequence = self.sequence
        return sequence[int(self.start_C):int(self.end_C)]

    def __str__(self):
        return 'Domain details added for: ' + self.accession

    # def fulllength(self):
    #     return self.sequence
    class Meta:
        ordering = ('accession',)
        verbose_name = 'Three domain detail'
        verbose_name_plural = "Three domain details"


class Description(models.Model):
    """
    """
    name = models.CharField(max_length=7)
    description = models.TextField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class UserUploadData(models.Model):
    """
    """
    session_key = models.CharField(max_length=250, default=None, null=True)
    name = models.CharField(max_length=250, null=True)
    sequence = models.TextField(null=True)

    def save(self, *args, **kwargs):
        if not self.name.endswith('_user'):
            self.name = self.name + '_user'
        super(UserUploadData, self).save(*args, **kwargs)

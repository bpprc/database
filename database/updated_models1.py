""" """

import textwrap

from Bio.SeqUtils.ProtParam import ProteinAnalysis
from django.contrib import admin
from django.core.files.base import ContentFile
from django.db import models
from django.utils import timezone


class PesticidalProteinDatabase(models.Model):
    """ """

    name = models.CharField(max_length=15, blank=True, null=False)
    oldname = models.CharField(max_length=105, blank=True, null=False)
    accession = models.CharField(max_length=25, blank=True, null=False)
    year = models.CharField(max_length=5, blank=True, null=False)
    sequence = models.TextField(blank=True, null=False)
    uploaded = models.DateTimeField("Uploaded", default=timezone.now)
    fastasequence_file = models.FileField(
        upload_to="fastasequence_files/", null=True, blank=True
    )

    class Meta:
        ordering = ("name",)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # TODO clear out old file before saving new one?
        filename = "fasta{}".format(self.name)
        file_contents = ">{}\n{}\n".format(
            self.name, self.fastasequence
        )
        # print(file_contents)
        content = ContentFile(file_contents)
        self.fastasequence_file.save(filename, content, save=False)
        super().save(*args, **kwargs)

    def category_name(self):
        return self.name[0][:3]

    def fastasequence(self):
        fasta = textwrap.fill(self.proteinsequence, 80)
        str_to_write = f"{self.name}\n{fasta}\n"
        return str_to_write

    def sequence_length(self):
        return len(self.sequence)

    def sequence_aromaticity(self):
        x = ProteinAnalysis(self.sequence)
        return x.aromaticity()

    def sequence_molecular_weight(self):
        x = ProteinAnalysis(self.sequence)
        return x.molecular_weight()

    def sequence_instability_index(self):
        x = ProteinAnalysis(self.sequence)
        return x.instability_index()

    def sequence_isoelectric_point(self):
        x = ProteinAnalysis(self.sequence)
        return x.isoelectric_point()

    def sequence_count_aminoacids(self):
        x = ProteinAnalysis(self.sequence)
        return x.count_amino_acids()  # how to draw histogram

    def sequence_get_amino_acids_percent(self):
        x = ProteinAnalysis(self.sequence)
        return x.get_amino_acids_percent()

    def sequence_charge_at_pH(self):
        pH = 4
        x = ProteinAnalysis(self.sequence, pH)
        return x.charge_at_pH


class ProteinDetail(models.Model):

    # name = models.ForeignKey(PesticidalProteinDatabase, related_name="%(class)s_name", on_delete=models.CASCADE,)
    # accession = models.ForeignKey(PesticidalProteinDatabase, related_name="%(class)s_accession", on_delete=models.CASCADE,)
    # sequence = models.ForeignKey(PesticidalProteinDatabase, related_name="%(class)s_fastasequence", on_delete=models.CASCADE,)
    accession = models.CharField(max_length=25, blank=True, null=False)
    fastasequence = models.TextField(blank=True, null=False)
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

    def get_endotoxin_n(self):
        if not self.start_N or not self.end_N:
            return ""
        fastasequence = self.fastasequence
        return fastasequence[int(self.start_N) : int(self.end_N)]

    def get_endotoxin_m(self):
        if not self.start_M or not self.end_M:
            return ""
        fastasequence = self.fastasequence
        return fastasequence[int(self.start_M) : int(self.end_M)]

    def get_endotoxin_c(self):
        if not self.start_C or not self.end_C:
            return ""
        fastasequence = self.fastasequence
        return fastasequence[int(self.start_C) : int(self.end_C)]


class Description(models.Model):
    """ """

    name = models.CharField(max_length=7)
    description = models.TextField()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class UserUploadData(models.Model):
    """ """

    session_key = models.CharField(max_length=40, default=None)
    name = models.CharField(max_length=15, blank=True, null=False)
    fastasequence = models.TextField(blank=True, null=False)


class FeedbackData(models.Model):
    """ """

    from_email = models.EmailField(max_length=75)
    subject = models.CharField(max_length=75)
    message = models.TextField(blank=True, null=False)

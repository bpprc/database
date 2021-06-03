""" """

import re
import textwrap

from Bio.SeqUtils.ProtParam import ProteinAnalysis
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.files.base import ContentFile
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from database.storage import OverwriteStorage

TRUE_FALSE_CHOICES = ((True, "Yes"), (False, "No"))


class OldnameNewnameTableLeft(models.Model):
    """
    Class representing a Old Name and New name Table.
    Organized by New Name.
    """

    # 2020 Nomenclature based names i.e. New Name of the proteins
    name_2020 = models.CharField(max_length=250, blank=True, null=True)

    # 1998 Nomenclature based names i.e. Old Name of the proteins
    name_1998 = models.CharField(max_length=250, blank=True, null=True)

    # Several different names of the same protein mentioned in the literature by various authors i.e. multiple names for the protein
    # Specially before the Nomenclature system (1998)
    alternative_name = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Organized by new name"
        verbose_name_plural = "Organized by new name"


class OldnameNewnameTableRight(models.Model):
    """
    Class representing a Old Name and New name Table.
    Organized by Old Name.
    """

    # 1998 Nomenclature based names i.e. Old Name of the proteins
    name_1998 = models.CharField(max_length=250, blank=True, null=True)

    # 2020 Nomenclature based names i.e. New Name of the proteins
    name_2020 = models.CharField(max_length=250, blank=True, null=True)

    # Several different names of the same protein mentioned
    # in the literature by various authors i.e. multiple
    # names for the protein
    # Specially before the Nomenclature system (1998)
    alternative_name = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Organized by Oldname"
        verbose_name_plural = "Organized by Oldname"


CHOICES = [
    ("yes", "Yes"),
    ("no", "No"),
]


class StructureDatabase(models.Model):
    """
    Structure database fields. The data is curated by Prof.Colin Berry.
    """

    # 2020 Nomenclature based names i.e. New Name of the proteins
    name = models.CharField(max_length=25, blank=True, null=True)

    # 1998 Nomenclature based names i.e. Old Name of the proteins
    oldname = models.CharField(max_length=75, blank=True, null=True)

    # National Center for Biotechnology Information (NCBI) accession number
    # https://www.ncbi.nlm.nih.gov/genbank/sequenceids/
    # https://www.ncbi.nlm.nih.gov/genbank/acc_prefix/
    accession = models.CharField(max_length=75, blank=True, null=True)

    # Protein Data Bank identifier
    # https://proteopedia.org/wiki/index.php/PDB_code
    # https://www.rcsb.org/pages/about-us/index
    pdbid = ArrayField(models.CharField(
        max_length=1000, null=True), default=list)

    # NCBI PubMed id
    # https://www.ncbi.nlm.nih.gov/pmc/pmctopmid/
    pubmedid = models.CharField(max_length=75, blank=True, null=True)

    # PDB id released year
    year = models.CharField(max_length=5, blank=True, null=True)

    # This field provides whether the protein sequence is modified or not
    # If modified "Yes" otherwise "No"
    modified = models.CharField(
        max_length=100, choices=CHOICES, default="Yes", blank=True, null=True)

    # Any other information related to the protein
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "Structure Information"
        verbose_name_plural = "Structure Database"


class PesticidalProteinHiddenSequence(models.Model):
    """
    Here’s a list of toxins that would be useful to add to the naming analysis as extra hidden seqs so that we get extra data for those sequences that don’t have good matches.  I’ve only put in one example each for TcA/B/C but that should be enough to show us if we have a match.  I’m afraid I don’t have accession numbers of most of these.
    """

    name = models.CharField(max_length=15, blank=True, null=True)
    oldname = models.CharField(max_length=305, blank=True, null=True)
    othernames = models.TextField(blank=True, null=True)
    accession = models.CharField(max_length=25, blank=True, null=True)
    year = models.CharField(max_length=5, blank=True, null=True)
    sequence = models.TextField(null=True)
    bacterium = models.BooleanField(
        default=True, choices=TRUE_FALSE_CHOICES, blank=True, null=True)
    bacterium_textbox = models.CharField(
        max_length=250, default="Bacillus Thuringiensis", blank=True, null=True)
    strain = models.CharField(max_length=250, blank=True, null=True)
    publication = models.TextField(null=True, blank=True)
    family = models.CharField(
        max_length=305, blank=True, null=True, default="None")
    toxicto = models.CharField(
        max_length=250, blank=True, null=True, default="None")
    nontoxic = models.CharField(max_length=250, blank=True, null=True)
    mammalian_active = models.CharField(
        max_length=250, blank=True, null=True)

    # Protein Data Bank identifier
    # https://proteopedia.org/wiki/index.php/PDB_code
    # https://www.rcsb.org/pages/about-us/index
    pdbcode = models.CharField(max_length=10, blank=True, null=True)
    comment = models.TextField(null=True, blank=True)
    submittersname = models.CharField(max_length=25, blank=True, null=True)
    submittersemail = models.EmailField(
        max_length=70, blank=True, null=True)
    taxonid = models.CharField(max_length=25, validators=[RegexValidator(
        r'\d{25}', 'Number must digits', 'Invalid number')], blank=True, null=True)
    partnerprotein = models.BooleanField(
        default=True, choices=TRUE_FALSE_CHOICES, blank=True, null=True)
    partnerprotein_textbox = models.CharField(
        max_length=250, blank=True, null=True)
    dnasequence = models.TextField(blank=True, null=True)
    uploaded = models.DateTimeField(
        "Uploaded", default=timezone.now, blank=True, null=True)
    alignresults = models.TextField(null=True, blank=True)
    predict_name = models.TextField(null=True, blank=True)
    terms_conditions = models.BooleanField(
        default=False, choices=TRUE_FALSE_CHOICES, blank=True, null=True)
    admin_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    admin_comments = models.TextField(null=True, blank=True)
    public = models.BooleanField(default=False, blank=True, null=True)
    # private = models.BooleanField(
    #     default=True, choices=TRUE_FALSE_CHOICES, blank=True, null=True)
    fastasequence_file = models.FileField(
        upload_to="fastasequence_files/", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Hidden sequence"
        verbose_name_plural = "Hidden sequences for naming purpose"


class PesticidalProteinPrivateDatabase(models.Model):
    """
    Private sequences are used only for the naming purpose. These protein sequences are unreleased to public. Once NCBI release's the sequence and the sequences are moved to public model.
    """

    # User who submits the sequence through "sequence submit form"
    submittersname = models.CharField(max_length=25, blank=True, null=True)

    # User corresponding email
    submittersemail = models.EmailField(max_length=70, blank=True, null=True)

    # 2020 Nomenclature New Name
    name = models.CharField(max_length=15, null=True,
                            verbose_name="Protein Name")

    # Protein sequence
    sequence = models.TextField(null=True, verbose_name="Protein Sequence")

    # Is it a bacterium sequence?. If the choice is "yes" then name of the
    # bacteria should be in the bacterium textbox. If the choice is "no" then explanation about the source.
    # Note: The BPPRC doesn't normally assign names to proteins that are not
    # of bacterial origin. If user wish to make a special case for the
    # sequence, the explanation can be stored in the text box.
    bacterium = models.BooleanField(
        default=True, choices=TRUE_FALSE_CHOICES, blank=True, null=True)
    bacterium_textbox = models.CharField(max_length=250, blank=True, null=True)

    # NCBI taxon id
    # https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi
    taxonid = models.CharField(max_length=25, validators=[RegexValidator(
        r'\d{25}', 'Number must digits', 'Invalid number')], blank=True, null=True)

    # Submission year
    year = models.CharField(max_length=5, null=True)

    # National Center for Biotechnology Information (NCBI) accession number
    # https://www.ncbi.nlm.nih.gov/genbank/sequenceids/
    # https://www.ncbi.nlm.nih.gov/genbank/acc_prefix/
    accession = models.CharField(
        max_length=25, null=True, verbose_name="NCBI accession number")

    # Partner protein required for toxicity?. If the choice is "yes", then
    # user can mention name of the protein
    partnerprotein = models.BooleanField(
        default=True, choices=TRUE_FALSE_CHOICES, blank=True, null=True)
    partnerprotein_textbox = models.CharField(
        max_length=250, blank=True, null=True)

    # If toxic to the organism. User can mention the name.
    toxicto = models.CharField(max_length=250, blank=True, null=True)

    # If nontoxic to the organism. User can mention the name.
    nontoxic = models.CharField(max_length=250, blank=True, null=True)

    # Correponding DNA sequence information
    dnasequence = models.TextField(blank=True, null=True)

    # Protein Data Bank identifier
    # https://proteopedia.org/wiki/index.php/PDB_code
    # https://www.rcsb.org/pages/about-us/index
    # Correponding PDB id
    pdbcode = models.CharField(max_length=10, blank=True, null=True)

    # DOI publication or PubMed ID or Publication text
    publication = models.TextField(blank=True, null=True)

    # Any other comments from user
    comment = models.TextField(
        blank=True, null=True, verbose_name="User comments")
    uploaded = models.DateTimeField(
        "Uploaded", default=timezone.now, blank=True, null=True)
    alignresults = models.TextField(blank=True, null=True)
    predict_name = models.TextField(blank=True, null=True)
    terms_conditions = models.BooleanField(
        default=False, choices=TRUE_FALSE_CHOICES, blank=True, null=True)
    admin_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    admin_comments = models.TextField(blank=True, null=True)

    # If the sequence is public
    public = models.BooleanField(default=False, null=True)

    # If the sequence is private
    # private = models.BooleanField(
    #     default=True, choices=TRUE_FALSE_CHOICES, null=True)
    oldname = models.CharField(max_length=105, blank=True, null=True)
    othernames = models.TextField(blank=True, null=True)
    fastasequence_file = models.FileField(
        upload_to="fastasequence_files/", null=True)
    name_category = models.CharField(max_length=15, blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_created_by",
        blank=True, null=True,
    )
    created_on = models.DateTimeField(
        "Created on", blank=True, null=True, default=timezone.now)
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name="%(class)s_edited_by",
    )
    edited_on = models.DateTimeField(
        "Edited on", blank=True, null=True, default=timezone.now)
    # published = models.BooleanField(default=True, choices=TRUE_FALSE_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "Private Sequence"
        verbose_name_plural = "Private Sequences"


class PesticidalProteinDatabase(models.Model):
    """
    Public sequences in the database.
    """

    # User who submits the sequence through "sequence submit form"
    submittersname = models.CharField(
        max_length=125, blank=True, null=True, default="Uploaded by default admin user")

    # User corresponding email
    submittersemail = models.EmailField(max_length=70, blank=True, null=True)

    # 2020 Nomenclature New Name
    name = models.CharField(max_length=15, null=True,
                            verbose_name="Protein Name")

    # 1998 Nomenclature name
    oldname = models.CharField(max_length=105, blank=True, null=True)

    # Several different names of the same protein mentioned in the literature by various authors i.e. multiple names for the protein
    # Specially before the Nomenclature system (1998)
    othernames = models.TextField(blank=True, null=True)

    # National Center for Biotechnology Information (NCBI) accession number
    # https://www.ncbi.nlm.nih.gov/genbank/sequenceids/
    # https://www.ncbi.nlm.nih.gov/genbank/acc_prefix/
    accession = models.CharField(
        max_length=25, null=True, verbose_name="NCBI accession number")

    # Sequence released year
    year = models.CharField(max_length=5, blank=True, null=True)

    # Protein sequence
    sequence = models.TextField(null=True, verbose_name="Protein Sequence")

    # Is it a bacterium sequence?. If the choice is "yes" then name of the
    # bacteria should be in the bacterium textbox. If the choice is "no" then explanation about the source.
    # Note: The BPPRC doesn't normally assign names to proteins that are not
    # of bacterial origin. If user wish to make a special case for the
    # sequence, the explanation can be stored in the text box.
    bacterium = models.BooleanField(
        default=True, choices=TRUE_FALSE_CHOICES, blank=True, null=True)

    # NCBI taxon id
    # https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi
    taxonid = models.CharField(max_length=25, validators=[RegexValidator(
        r'\d{25}', 'Number must digits', 'Invalid number')], blank=True, null=True)

    bacterium_textbox = models.CharField(max_length=250, blank=True, null=True)

    # Partner protein required for toxicity?. If the choice is "yes", then
    # user can mention name of the protein
    partnerprotein = models.BooleanField(
        default=True, choices=TRUE_FALSE_CHOICES, blank=True, null=True)
    partnerprotein_textbox = models.CharField(
        max_length=250, blank=True, null=True)

    # If toxic to the organism. User can mention the name.
    toxicto = models.CharField(max_length=250, blank=True, null=True)

    # If nontoxic to the organism. User can mention the name.
    nontoxic = models.CharField(max_length=250, blank=True, null=True)

    # Correponding DNA sequence information
    dnasequence = models.TextField(blank=True, null=True)

    # DOI publication or PubMed ID or Publication text
    publication = models.TextField(blank=True, null=True)
    comment = models.TextField(
        blank=True, null=True, verbose_name="User comments")
    uploaded = models.DateTimeField("Uploaded", default=timezone.now)
    fastasequence_file = models.FileField(
        upload_to="fastasequence_files/", storage=OverwriteStorage(), null=True)
    name_category = models.CharField(max_length=15, blank=True, null=True)

    # If the sequence is public or not, based on the boolean operator
    public = models.BooleanField(default=True, null=True)

    # Protein Data Bank identifier
    # https://proteopedia.org/wiki/index.php/PDB_code
    # https://www.rcsb.org/pages/about-us/index
    pdbcode = models.CharField(max_length=10, blank=True, null=True)
    predict_name = models.TextField(blank=True, null=True)

    # Whether user accepted BPPRC terms & conditions
    terms_conditions = models.BooleanField(
        default=False, choices=TRUE_FALSE_CHOICES, blank=True, null=True)

    # Admin user who submits the sequence
    admin_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    # Admin user comments for future reference
    admin_comments = models.TextField(blank=True, null=True)

    # Audit entries details. This is similar to log entry for the sequence
    # Information like who edited the sequence or modified the field are
    # logged automatically
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_created_by",
        blank=True, null=True
    )
    created_on = models.DateTimeField(
        "Created on", blank=True, null=True, default=timezone.now)
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name="%(class)s_edited_by",
    )
    edited_on = models.DateTimeField(
        "Edited on", blank=True, null=True, default=timezone.now)
    published = models.BooleanField(
        default=False, choices=TRUE_FALSE_CHOICES, blank=True, null=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Public Sequence"
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
        filename = "{}".format(self.name)
        file_contents = ">{}\n{}\n".format(self.name, self.sequence)
        # print(file_contents)
        content = ContentFile(file_contents)
        self.fastasequence_file.save(filename, content, save=False)
        super().save(*args, **kwargs)

    def category_name(self):
        return self.name[:3]

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
        # x = x.molecular_weight()
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


class ProteinDetail(models.Model):

    """
    The domain information from NCBI. NCBI has sequence features like source organism, protein regions (region name and corresponding sequence number).
    Example:
    https://www.ncbi.nlm.nih.gov/protein/BAA04468#feature_BAA04468.1_Region_0

    The provided example above accession number is BAA04468.1. If access the link, one can see the FEATURES section where the information are
    source          1..1176
                     /organism="Bacillus thuringiensis"
                     /strain="FU-2-7"
                     /db_xref="taxon:1428"
     Protein         1..1176
                     /product="insecticidal crystal protein"
     Region          48..251
                     /region_name="Endotoxin_N"
                     /note="delta endotoxin, N-terminal domain; pfam03945"
                     /db_xref="CDD:281878"
     Region          259..460
                     /region_name="Endotoxin_M"
                     /note="delta endotoxin; pfam00555"
                     /db_xref="CDD:278954"
     Region          462..605
                     /region_name="delta_endotoxin_C"
                     /note="delta-endotoxin C-terminal domain may be associated
                     with carbohydrate binding functionality; cd04085"
                     /db_xref="CDD:271151"
    These information are extracted for all the accession number (if the information is available) added to the model. These sequence information is used to draw guided tree.
    """

    # 2020 Nomenclature New Name
    name = models.CharField(max_length=25, null=True)

    # National Center for Biotechnology Information (NCBI) accession number
    # https://www.ncbi.nlm.nih.gov/genbank/sequenceids/
    # https://www.ncbi.nlm.nih.gov/genbank/acc_prefix/
    accession = models.CharField(max_length=25, null=True)

    # Protein sequence
    sequence = models.TextField(null=True)

    # Length of the protein sequence
    fulllength = models.TextField(null=True)

    # Source organism
    species = models.TextField(null=True)

    # NCBI taxon id
    # https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi
    taxon = models.TextField(null=True)

    # Domain 1 information
    # N-terminal information length (domain_N)
    # N-terminal Protein family database (pfam) domain id
    # Pfam link https://pfam.xfam.org/about
    # N-terminal Conserved Domain Database (cdd) id
    # CDD link https://www.ncbi.nlm.nih.gov/Structure/cdd/cdd.shtml
    # Start position number of the N-terminal
    # End position number of the N-terminal
    domain_N = models.TextField(null=True)
    pfam_N = models.CharField(max_length=25, null=True)
    cdd_N = models.CharField(max_length=25, null=True)
    start_N = models.CharField(max_length=10, null=True)
    end_N = models.CharField(max_length=10, null=True)

    # Domain 2 information
    # Middle domain information length (domain_M)
    # Middle domain Protein family database (pfam) domain id
    # Pfam link https://pfam.xfam.org/about
    # Middle domain Conserved Domain Database (cdd) id
    # CDD link https://www.ncbi.nlm.nih.gov/Structure/cdd/cdd.shtml
    # Start position number of the Middle domain
    # End position number of the Middle domain
    domain_M = models.TextField(null=True)
    pfam_M = models.CharField(max_length=25, null=True)
    cdd_M = models.CharField(max_length=25, null=True)
    start_M = models.CharField(max_length=10, null=True)
    end_M = models.CharField(max_length=10, null=True)

    # Domain 3 information
    # C-terminal information length (domain_C)
    # C-terminal Protein family database (pfam) domain id
    # Pfam link https://pfam.xfam.org/about
    # C-terminal Conserved Domain Database (cdd) id
    # CDD link https://www.ncbi.nlm.nih.gov/Structure/cdd/cdd.shtml
    # Start position number of the C-terminal
    # End position number of the C-terminal
    domain_C = models.TextField(null=True)
    pfam_C = models.CharField(max_length=25, null=True)
    cdd_C = models.CharField(max_length=10, null=True)
    start_C = models.CharField(max_length=10, null=True)
    end_C = models.CharField(max_length=10, null=True)

    def save(self, *args, **kwargs):
        p = PesticidalProteinDatabase.objects.get(accession=self.accession)
        super(ProteinDetail).save(*args, **kwargs)
        ProteinDetail.filter(pk=self.pk).update(name=p.name)

    def get_endotoxin_n(self):
        if not self.start_N or not self.end_N:
            return ""
        sequence = self.sequence
        return sequence[int(self.start_N): int(self.end_N)]

    def get_endotoxin_m(self):
        if not self.start_M or not self.end_M:
            return ""
        sequence = self.sequence
        return sequence[int(self.start_M): int(self.end_M)]

    def get_endotoxin_c(self):
        if not self.start_C or not self.end_C:
            return ""
        sequence = self.sequence
        return sequence[int(self.start_C): int(self.end_C)]

    def __str__(self):
        return "Domain details added for: " + self.accession

    # def fulllength(self):
    #     return self.sequence
    class Meta:
        ordering = ("accession",)
        verbose_name = "Three domain detail"
        verbose_name_plural = "Three domain details"


class Description(models.Model):
    """
    Protein structure class descriptions
    Ex. App : Pesticidal proteins with a predominately Alpha helical structure, e.g. those previously known as Cry6
    """

    name = models.CharField(max_length=7)
    description = models.TextField()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class UserUploadData(models.Model):
    """
    Clustal analysis
    link: http://www.clustal.org/omega/
    After the user adds to the cart. User can upload their sequence for the analysis. The model saves name, sequence, as well as session key to retrieve the tree later.
    """

    session_key = models.CharField(max_length=250, default=None, null=True)
    name = models.CharField(max_length=250, null=True)
    sequence = models.TextField(null=True)

    def save(self, *args, **kwargs):
        if not self.name.endswith("_user"):
            self.name = self.name + "_user"
        super(UserUploadData, self).save(*args, **kwargs)

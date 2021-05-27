# Generated by Django 3.1.4 on 2021-05-07 06:14

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("database", "0003_auto_20210503_2150"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="accession",
            field=models.CharField(
                max_length=25,
                null=True,
                verbose_name="NCBI accession number",
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="admin_comments",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="admin_user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="bacterium",
            field=models.BooleanField(
                choices=[(True, "Yes"), (False, "No")],
                default=True,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="bacterium_textbox",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="comment",
            field=models.TextField(
                null=True, verbose_name="User comments"
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="created_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pesticidalproteindatabase_created_by",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="created_on",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                null=True,
                verbose_name="Created on",
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="dnasequence",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="edited_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pesticidalproteindatabase_edited_by",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="edited_on",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                null=True,
                verbose_name="Edited on",
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="fastasequence_file",
            field=models.FileField(
                null=True, upload_to="fastasequence_files/"
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="name",
            field=models.CharField(
                max_length=15, null=True, verbose_name="Protein Name"
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="name_category",
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="nontoxic",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="oldname",
            field=models.CharField(max_length=105, null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="othernames",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="partnerprotein",
            field=models.BooleanField(
                choices=[(True, "Yes"), (False, "No")],
                default=True,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="partnerprotein_textbox",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="pdbcode",
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="predict_name",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="public",
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="publication",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="published",
            field=models.BooleanField(
                choices=[(True, "Yes"), (False, "No")],
                default=False,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="sequence",
            field=models.TextField(
                null=True, verbose_name="Protein Sequence"
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="submittersemail",
            field=models.EmailField(max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="submittersname",
            field=models.CharField(
                default="Uploaded by Suresh", max_length=125, null=True
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="taxonid",
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="terms_conditions",
            field=models.BooleanField(
                choices=[(True, "Yes"), (False, "No")],
                default=False,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="toxicto",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteindatabase",
            name="year",
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinhiddensequence",
            name="accession",
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinhiddensequence",
            name="bacterium",
            field=models.BooleanField(
                choices=[(True, "Yes"), (False, "No")],
                default=True,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinhiddensequence",
            name="bacterium_textbox",
            field=models.CharField(
                default="Bacillus Thuringiensis",
                max_length=250,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinhiddensequence",
            name="family",
            field=models.CharField(
                default="None", max_length=305, null=True
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinhiddensequence",
            name="mammalian_active",
            field=models.CharField(
                default="None", max_length=250, null=True
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinhiddensequence",
            name="name",
            field=models.CharField(
                default="None", max_length=15, null=True
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinhiddensequence",
            name="nontoxic",
            field=models.CharField(
                default="None", max_length=250, null=True
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinhiddensequence",
            name="oldname",
            field=models.CharField(
                default="None", max_length=305, null=True
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinhiddensequence",
            name="othernames",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinhiddensequence",
            name="partnerprotein",
            field=models.BooleanField(
                choices=[(True, "Yes"), (False, "No")],
                default=True,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinhiddensequence",
            name="partnerprotein_textbox",
            field=models.CharField(
                default="None", max_length=250, null=True
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinhiddensequence",
            name="pdbcode",
            field=models.CharField(
                default="None", max_length=10, null=True
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinhiddensequence",
            name="private",
            field=models.BooleanField(
                choices=[(True, "Yes"), (False, "No")],
                default=True,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinhiddensequence",
            name="public",
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinhiddensequence",
            name="strain",
            field=models.CharField(
                default="None", max_length=250, null=True
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinhiddensequence",
            name="submittersemail",
            field=models.EmailField(
                default="None", max_length=70, null=True
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinhiddensequence",
            name="submittersname",
            field=models.CharField(
                default="None", max_length=25, null=True
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinhiddensequence",
            name="taxonid",
            field=models.CharField(
                default="None", max_length=25, null=True
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinhiddensequence",
            name="terms_conditions",
            field=models.BooleanField(
                choices=[(True, "Yes"), (False, "No")],
                default=False,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinhiddensequence",
            name="toxicto",
            field=models.CharField(
                default="None", max_length=250, null=True
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinhiddensequence",
            name="uploaded",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                null=True,
                verbose_name="Uploaded",
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinhiddensequence",
            name="year",
            field=models.CharField(
                default="None", max_length=5, null=True
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="accession",
            field=models.CharField(
                max_length=25,
                null=True,
                verbose_name="NCBI accession number",
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="admin_comments",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="admin_user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="alignresults",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="bacterium",
            field=models.BooleanField(
                choices=[(True, "Yes"), (False, "No")],
                default=True,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="bacterium_textbox",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="comment",
            field=models.TextField(
                null=True, verbose_name="User comments"
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="created_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pesticidalproteinprivatedatabase_created_by",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="created_on",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                null=True,
                verbose_name="Created on",
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="edited_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pesticidalproteinprivatedatabase_edited_by",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="edited_on",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                null=True,
                verbose_name="Edited on",
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="fastasequence_file",
            field=models.FileField(
                null=True, upload_to="fastasequence_files/"
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="name",
            field=models.CharField(
                max_length=15, null=True, verbose_name="Protein Name"
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="name_category",
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="nontoxic",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="oldname",
            field=models.CharField(max_length=105, null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="othernames",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="partnerprotein",
            field=models.BooleanField(
                choices=[(True, "Yes"), (False, "No")],
                default=True,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="partnerprotein_textbox",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="pdbcode",
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="predict_name",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="private",
            field=models.BooleanField(
                choices=[(True, "Yes"), (False, "No")],
                default=True,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="public",
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="publication",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="sequence",
            field=models.TextField(
                null=True, verbose_name="Protein Sequence"
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="submittersname",
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="taxonid",
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="terms_conditions",
            field=models.BooleanField(
                choices=[(True, "Yes"), (False, "No")],
                default=False,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="toxicto",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="uploaded",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                null=True,
                verbose_name="Uploaded",
            ),
        ),
        migrations.AlterField(
            model_name="pesticidalproteinprivatedatabase",
            name="year",
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name="proteindetail",
            name="accession",
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="proteindetail",
            name="cdd_C",
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="proteindetail",
            name="cdd_M",
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="proteindetail",
            name="cdd_N",
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="proteindetail",
            name="domain_C",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="proteindetail",
            name="domain_M",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="proteindetail",
            name="domain_N",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="proteindetail",
            name="end_C",
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="proteindetail",
            name="end_M",
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="proteindetail",
            name="end_N",
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="proteindetail",
            name="fulllength",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="proteindetail",
            name="name",
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="proteindetail",
            name="pfam_C",
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="proteindetail",
            name="pfam_M",
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="proteindetail",
            name="pfam_N",
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="proteindetail",
            name="sequence",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="proteindetail",
            name="species",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="proteindetail",
            name="start_C",
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="proteindetail",
            name="start_M",
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="proteindetail",
            name="start_N",
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="proteindetail",
            name="taxon",
            field=models.TextField(null=True),
        ),
    ]

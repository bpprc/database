# Generated by Django 2.2.6 on 2020-07-11 16:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BacteriaTaxonID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taxonid', models.CharField(blank=True, max_length=250, null=True)),
                ('bacterianame', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submittersname', models.CharField(blank=True, max_length=25, null=True)),
                ('submittersemail', models.EmailField(max_length=70, null=True)),
                ('proteinname', models.CharField(blank=True, max_length=25, null=True)),
                ('proteinsequence', models.TextField(null=True)),
                ('bacterium', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=True)),
                ('bacterium_textbox', models.CharField(blank=True, max_length=250, null=True)),
                ('taxonid', models.CharField(blank=True, max_length=25, null=True)),
                ('year', models.CharField(blank=True, max_length=4, null=True)),
                ('accessionnumber', models.CharField(blank=True, max_length=25)),
                ('partnerprotein', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=True)),
                ('partnerprotein_textbox', models.CharField(blank=True, max_length=250, null=True)),
                ('toxicto', models.CharField(blank=True, max_length=250)),
                ('nontoxic', models.CharField(blank=True, max_length=250)),
                ('dnasequence', models.TextField(null=True)),
                ('pdbcode', models.CharField(blank=True, max_length=10)),
                ('publication', models.TextField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('uploaded', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Uploaded')),
                ('alignresults', models.TextField(blank=True, null=True)),
                ('predict_name', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ('submittersemail',),
            },
        ),
    ]

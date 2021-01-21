# Generated by Django 3.1.4 on 2021-01-21 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Association',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, verbose_name='Protein Name')),
                ('oldname', models.TextField(blank=True, verbose_name='Old Name')),
                ('accession', models.TextField(blank=True, verbose_name='NCBI accession number')),
                ('partnerprotein', models.CharField(default='No', max_length=7)),
                ('partnerprotein_textbox', models.TextField(blank=True)),
                ('target_order', models.TextField(blank=True)),
                ('target_species', models.TextField(blank=True, null=True)),
                ('activity', models.CharField(default='Yes', max_length=7)),
                ('taxonid', models.TextField(blank=True)),
                ('lc50', models.TextField(blank=True)),
                ('units', models.TextField(blank=True)),
                ('non_toxic', models.TextField(blank=True)),
                ('percentage_mortality', models.TextField(blank=True)),
                ('publication', models.TextField(blank=True)),
                ('other_citations', models.TextField(blank=True)),
                ('life_stage', models.TextField(blank=True)),
                ('instar', models.TextField(blank=True)),
                ('assay_material', models.TextField(blank=True)),
                ('assay_method', models.TextField(blank=True)),
                ('comment', models.TextField(blank=True)),
                ('data_entered_by', models.TextField(blank=True)),
            ],
        ),
    ]

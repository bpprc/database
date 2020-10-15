# Generated by Django 2.2 on 2020-10-15 14:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PesticidalProteinHiddenSequence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=15)),
                ('oldname', models.CharField(blank=True, max_length=105)),
                ('othernames', models.TextField(blank=True)),
                ('accession', models.CharField(blank=True, max_length=25)),
                ('year', models.CharField(blank=True, max_length=5)),
                ('sequence', models.TextField(blank=True)),
                ('uploaded', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Uploaded')),
                ('fastasequence_file', models.FileField(blank=True, null=True, upload_to='fastasequence_files/')),
                ('public', models.BooleanField(default=False)),
            ],
        ),
    ]

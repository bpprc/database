# Generated by Django 2.2 on 2020-10-19 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_pesticidalproteinhiddensequence'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PesticidalProteinStructureDatabase',
            new_name='StructureDatabase',
        ),
    ]

# Generated by Django 3.1.4 on 2021-02-15 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('association', '0002_auto_20210213_1536'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='association',
            name='accession',
        ),
        migrations.RemoveField(
            model_name='association',
            name='oldname',
        ),
    ]
# Generated by Django 2.2.6 on 2020-08-24 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0009_remove_proteindetail_sequence'),
    ]

    operations = [
        migrations.AddField(
            model_name='proteindetail',
            name='sequence',
            field=models.TextField(blank=True),
        ),
    ]
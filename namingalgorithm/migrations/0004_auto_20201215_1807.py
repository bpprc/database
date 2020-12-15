# Generated by Django 3.1.4 on 2020-12-15 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('namingalgorithm', '0003_auto_20201215_1131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='archive',
            name='alignresults',
        ),
        migrations.RemoveField(
            model_name='usersubmission',
            name='alignresults',
        ),
        migrations.AlterField(
            model_name='archive',
            name='predict_name',
            field=models.TextField(blank=True, null=True, verbose_name='Predicted Name'),
        ),
        migrations.AlterField(
            model_name='usersubmission',
            name='predict_name',
            field=models.TextField(blank=True, null=True, verbose_name='Predicted Name'),
        ),
    ]

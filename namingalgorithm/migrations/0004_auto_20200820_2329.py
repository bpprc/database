# Generated by Django 2.2.6 on 2020-08-20 23:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('namingalgorithm', '0003_auto_20200820_2324'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersubmission',
            name='date',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='usersubmission',
            name='uploaded',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Uploaded'),
        ),
    ]
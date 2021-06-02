# Generated by Django 3.1.3 on 2021-06-02 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('namingalgorithm', '0002_auto_20210602_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archive',
            name='contact_status',
            field=models.CharField(choices=[('emailed', 'Emailed'), ('pending', 'Pending')], default='Pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='usersubmission',
            name='contact_status',
            field=models.CharField(choices=[('emailed', 'Emailed'), ('pending', 'Pending')], default='Pending', max_length=10),
        ),
    ]
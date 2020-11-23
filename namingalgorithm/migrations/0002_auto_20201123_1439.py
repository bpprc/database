# Generated by Django 3.1.3 on 2020-11-23 19:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('namingalgorithm', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='archive',
            old_name='accessionnumber',
            new_name='accession',
        ),
        migrations.RenameField(
            model_name='archive',
            old_name='proteinname',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='archive',
            old_name='proteinsequence',
            new_name='sequence',
        ),
        migrations.RenameField(
            model_name='sendemail',
            old_name='proteinname',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='usersubmission',
            old_name='accessionnumber',
            new_name='accession',
        ),
        migrations.RenameField(
            model_name='usersubmission',
            old_name='proteinname',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='usersubmission',
            old_name='proteinsequence',
            new_name='sequence',
        ),
        migrations.AddField(
            model_name='archive',
            name='admin_comments',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='archive',
            name='admin_user',
            field=models.ForeignKey(blank=True, default='1', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='archive',
            name='private',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=True),
        ),
        migrations.AddField(
            model_name='archive',
            name='user_provided_proteinname',
            field=models.CharField(blank=True, max_length=105),
        ),
        migrations.AddField(
            model_name='usersubmission',
            name='admin_comments',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usersubmission',
            name='admin_user',
            field=models.ForeignKey(blank=True, default='1', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usersubmission',
            name='private',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=True),
        ),
        migrations.AddField(
            model_name='usersubmission',
            name='user_provided_proteinname',
            field=models.CharField(blank=True, max_length=105),
        ),
        migrations.AlterField(
            model_name='archive',
            name='terms_conditions',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False),
        ),
        migrations.AlterField(
            model_name='usersubmission',
            name='terms_conditions',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False),
        ),
    ]

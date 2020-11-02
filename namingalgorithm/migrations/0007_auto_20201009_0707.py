# Generated by Django 2.2 on 2020-10-09 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('namingalgorithm', '0006_usersubmission_terms_conditions'),
    ]

    operations = [
        migrations.CreateModel(
            name='SendEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submittersname', models.CharField(blank=True, max_length=25, null=True)),
                ('submittersemail', models.EmailField(max_length=70, null=True)),
                ('proteinname', models.CharField(blank=True, max_length=25, null=True)),
                ('message', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='usersubmission',
            name='terms_conditions',
            field=models.BooleanField(default=False),
        ),
    ]
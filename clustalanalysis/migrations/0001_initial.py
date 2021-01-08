# Generated by Django 3.1.4 on 2021-01-07 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StoreResultFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taskid', models.CharField(blank=True, max_length=250)),
                ('tempfile', models.CharField(max_length=1000, null=True)),
                ('resultfile', models.FileField(blank=True, null=True, upload_to='store_result_files/')),
            ],
            options={
                'verbose_name': 'Store result file',
                'verbose_name_plural': 'Store results files',
            },
        ),
    ]

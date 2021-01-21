# Generated by Django 3.1.4 on 2021-01-21 14:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=75, null=True)),
                ('subject', models.CharField(blank=True, max_length=75, null=True)),
                ('email', models.EmailField(max_length=70, null=True)),
                ('message', models.TextField(blank=True)),
                ('uploaded', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Uploaded')),
            ],
            options={
                'verbose_name': 'Feedback',
                'verbose_name_plural': 'Feedback',
            },
        ),
    ]

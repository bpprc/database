# Generated by Django 3.1.4 on 2021-05-10 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extra', '0002_externallinks'),
    ]

    operations = [
        migrations.AddField(
            model_name='externallinks',
            name='description',
            field=models.TextField(default='None'),
        ),
    ]

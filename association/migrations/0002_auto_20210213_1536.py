# Generated by Django 3.1.4 on 2021-02-13 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('association', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='association',
            options={'verbose_name': 'Association data'},
        ),
        migrations.AddField(
            model_name='association',
            name='non_toxic',
            field=models.TextField(blank=True),
        ),
    ]
# Generated by Django 3.1.4 on 2021-05-04 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("association", "0003_auto_20210215_1000"),
    ]

    operations = [
        migrations.AlterField(
            model_name="association",
            name="partnerprotein_textbox",
            field=models.TextField(blank=True, default="No"),
        ),
    ]

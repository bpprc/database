import csv

from django.conf.urls.static import settings, static
from django.core.management.base import BaseCommand

# Import the model
from association.models import Association

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the Association data from the CSV file, first delete the POSTGRES data file to destroy the database. Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Loads data from Association.csv"

    def handle(self, *args, **kwargs):

        file_path = settings.MEDIA_ROOT + "/csv_files/Association.csv"
        print("file path", file_path)
        # Show this if the data already exist in the database
        if Association.objects.exists():
            print("Data already loaded...exiting.")
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        # Show this before loading the data into the database
        print("Loading Association data")

        # Load the data into the database
        fields = [
            "name",
            "partnerprotein",
            "partnerprotein_textbox",
            "target_order",
            "target_species",
            "taxonid",
            "activity",
            "lc50",
            "units",
            "percentage_mortality",
            "publication",
            "other_citations",
            "life_stage",
            "instar",
            "assay_material",
            "assay_method",
            "comment",
            "data_entered_by",
        ]

        file_path = settings.MEDIA_ROOT + "/csv_files/Association.csv"
        print("file path", file_path)
        raw_data = open(file_path, "rt", encoding="utf-8-sig")
        for row in csv.reader(raw_data):
            Association.objects.create(**dict(zip(fields, row)))

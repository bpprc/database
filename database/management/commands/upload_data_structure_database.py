import csv

from django.conf.urls.static import settings, static
from django.core.management.base import BaseCommand

# Import the model
from database.models import StructureDatabase as PD

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the StructureDatabase data from the CSV file, first delete the POSTGRES data file to destroy the database. Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Loads data from StructureDatabase.csv"

    def handle(self, *args, **kwargs):

        file_path = settings.MEDIA_ROOT + "/csv_files/StructureDatabase.csv"
        print("file path", file_path)
        # Show this if the data already exist in the database
        if PD.objects.exists():
            print("Data already loaded...exiting.")
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        # Show this before loading the data into the database
        print("Loading StructureDatabase data")

        # Load the data into the database
        fields = [
            "name",
            "oldname",
            "accession",
            "pdbid",
            "pubmedid",
            "year",
            "modified",
            "comment",
        ]
        file_path = settings.MEDIA_ROOT + "/csv_files/StructureDatabase.csv"
        print("file path", file_path)
        raw_data = open(file_path, "rt", encoding="utf-8-sig")
        for row in csv.reader(raw_data):
            PD.objects.create(**dict(zip(fields, row)))

import csv

from django.conf.urls.static import settings
from django.core.management.base import BaseCommand

# Import the model
from namingalgorithm.models import UserSubmission

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the usersubmissions data from the CSV file, first delete the POSTGRES data file to destroy the database. Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Loads data from UserSubmission.csv"

    def handle(self, *args, **kwargs):

        file_path = settings.MEDIA_ROOT + "/csv_files/UserSubmission.csv"
        print("file path", file_path)
        # Show this if the data already exist in the database
        if UserSubmission.objects.exists():
            print("Data already loaded...exiting.")
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        # Show this before loading the data into the database
        print("Loading UserSubmission data")

        # Load the data into the database
        fields = [
            "submittersname",
            "submittersemail",
            "name",
            "sequence",
            "bacterium",
            "bacterium_textbox",
            "taxonid",
            "year",
            "accession",
            "dnasequence",
            "publication",
            "comment",
        ]

        file_path = settings.MEDIA_ROOT + "/csv_files/UserSubmission.csv"
        print("file path", file_path)
        raw_data = open(file_path, "rt", encoding="utf-8-sig")
        for row in csv.reader(raw_data):
            UserSubmission.objects.create(**dict(zip(fields, row)))

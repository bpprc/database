from django.core.management.base import BaseCommand
from django.conf.urls.static import static, settings
import csv

# Import the model
from database.models import ProteinDetail as PD

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the ProteinDetail-threedomains data from the CSV file, first delete the POSTGRES data file to destroy the database. Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = 'Loads data from ProteinDetail-threedomains.csv'

    def handle(self, *args, **kwargs):

        file_path = settings.MEDIA_ROOT + '/csv_files/ProteinDetail-threedomains.csv'
        print("file path", file_path)
        # Show this if the data already exist in the database
        if PD.objects.exists():
            print('Data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        # Show this before loading the data into the database
        print("Loading three domain data")

        # Load the data into the database
        fields = ['accession', 'sequence', 'fulllength', 'species', 'taxon', 'domain_N', 'pfam_N', 'cdd_N', 'start_N',
                  'end_N', 'domain_M', 'pfam_M', 'cdd_M', 'start_M', 'end_M', 'domain_C', 'pfam_C', 'cdd_C', 'start_C', 'end_C']

        file_path = settings.MEDIA_ROOT + '/csv_files/ProteinDetail-threedomains.csv'
        print("file path", file_path)
        raw_data = open(file_path, 'rt', encoding='utf-8-sig')
        for row in csv.reader(raw_data):
            PD.objects.create(**dict(zip(fields, row)))

from django.core.management.base import BaseCommand
from django.conf.urls.static import static, settings
import csv

# Import the model
from database.models import PesticidalProteinPrivateDatabase as PD

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the PesticidalProteinPrivateDatabase data from the CSV file, first delete the POSTGRES data file to destroy the database. Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = 'Loads data from PesticidalProteinPrivateDatabase.csv. Please provide filename along with the path'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='filename for csv file')

    def handle(self, *args, **kwargs):
        filename = kwargs['filename']

        file_path = settings.MEDIA_ROOT + '/csv_files/' + filename
        print("file path", file_path)
        # Show this if the data already exist in the database
        if PD.objects.exists():
            print('Data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        # Show this before loading the data into the database
        print("Loading PesticidalProteinPrivateDatabase data")

        # Load the data into the database
        fields = ['name', 'oldname', 'othernames',
                  'accession', 'year', 'sequence']
        file_path = settings.MEDIA_ROOT + '/csv_files/' + filename
        print("file path", file_path)
        raw_data = open(file_path, 'rt', encoding='utf-8-sig')
        for row in csv.reader(raw_data):
            PD.objects.create(**dict(zip(fields, row)))

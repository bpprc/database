from django.core.management.base import BaseCommand

from association.models import Association
from database.models import (
    Description,
    OldnameNewnameTableLeft,
    OldnameNewnameTableRight,
    PesticidalProteinDatabase,
    PesticidalProteinPrivateDatabase,
    ProteinDetail,
    StructureDatabase,
    UserUploadData,
)


class Command(BaseCommand):
    help = "Clear all the model data"

    def handle(self, *args, **options):
        PesticidalProteinDatabase.objects.all().delete()
        StructureDatabase.objects.all().delete()
        UserUploadData.objects.all().delete()
        Description.objects.all().delete()
        ProteinDetail.objects.all().delete()
        PesticidalProteinPrivateDatabase.objects.all().delete()
        OldnameNewnameTableLeft.objects.all().delete()
        OldnameNewnameTableRight.objects.all().delete()
        Association.objects.all().delete()
        PesticidalProteinHiddenSequence.objects.all().delete()

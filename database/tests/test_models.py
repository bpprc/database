from django.test import TestCase
from database.models import PesticidalProteinDatabase


class PesticidalProteinDatabaseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        PesticidalProteinDatabase.objects.create(
            name="Cry1001Aa1", oldname="R1")

    def test_name_label(self):
        protein = PesticidalProteinDatabase.objects.get(id=1)
        field_label = PesticidalProteinDatabase._meta.get_field(
            'name').verbose_name
        self.assertEquals(field_label, 'Protein Name')

    def test_name_max_length(self):
        protein = PesticidalProteinDatabase.objects.get(id=1)
        max_length = PesticidalProteinDatabase._meta.get_field(
            'name').max_length
        self.assertEquals(max_length, 15)

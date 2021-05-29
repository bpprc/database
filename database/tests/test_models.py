from django.test import TestCase

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


class PesticidalProteinDatabaseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        PesticidalProteinDatabase.objects.create(
            name="Cry1001Aa1", oldname="R1"
        )

    def test_name_label(self):
        protein = PesticidalProteinDatabase.objects.get(id=1)
        field_label = PesticidalProteinDatabase._meta.get_field(
            "name"
        ).verbose_name
        self.assertEquals(field_label, "Protein Name")

    def test_name_max_length(self):
        protein = PesticidalProteinDatabase.objects.get(id=1)
        max_length = PesticidalProteinDatabase._meta.get_field(
            "name"
        ).max_length
        self.assertEquals(max_length, 15)

    def setUp(self):
        self.database = PesticidalProteinDatabase.objects.create(
            submittersname="Suresh",
            submittersemail="admin@bpprc.org",
            name="Rpp1001Aa1",
            oldname="",
            othernames="",
            accession="M7829DHR",
            year="2023",
            sequence="MEKYMLLAQFPAEKTLNETDIPSATLQLLTGKQAGVARPGGIFTKEDLINIKLYV",
            bacterium="True",
            bacterium_textbox="Photorhabdus khanii",
            taxonid="1004151",
            partnerprotein="False",
            partnerprotein_textbox="",
            toxicto="",
            nontoxic="",
            dnasequence="",
            publication="",
        )

    def test_post_model(self):
        data = self.database
        self.assertTrue(isinstance(data, PesticidalProteinDatabase))

    def test_PesticidalProteinDatabase_name(self):
        database = self.database
        self.assertEqual(database.__str__(), "Rpp1001Aa1")

    def test_category_name(self):
        database = str(self.database.name)
        print(database[:3])
        category_name = database[:3]
        self.assertEqual(category_name, "Rpp")

from django.test import TestCase, Client
from django.urls import reverse
from database.models import PesticidalProteinDatabase, Description
import json


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.statistics_url = reverse('statistics')
        self.categorize_database_url = reverse(
            'categorize_database', args=['Cry'])
        self.protein_description = Description.objects.create(
            name='Cry',
            description='Mnemonic retained for 3-domain proteins'
        )
        self.protein_example = PesticidalProteinDatabase.objects.create(
            name='Cry1Aa1',
            oldname='Cry1Aa1',
            othernames='Cry1A(a)',
            accession='AAA22353',
            year='1985',
            sequence="""
            MDNNPNINECIPYNCLSNPEVEVLGGERIETGYTPIDISLSLTQFLLSEFVPGAGFVLGLVDIIWGIFGPSQWDAFPVQIEQLINQRIEEFARNQAISRLEGLSNLYQIYAESFREWEADPTNPALREEMRIQFNDMNSALTTAIPLLAVQNYQVPLLSVYVQAANLHLSVLRDVSVFGQRWGFDAATINSRYNDLTRLIGNYTDYAVRWYNTGLERVWGPDSRDWVRYNQFRRELTLTVLDIVALFSNYDSRRYPIRTVSQLTREIYTNPVLENFDGSFRGMAQRIEQNIRQPHLMDILNSITIYTDVHRGFNYWSGHQITASPVGFSGPEFAFPLFGNAGNAAPPVLVSLTGLGIFRTLSSPLYRRIILGSGPNNQELFVLDGTEFSFASLTTNLPSTIYRQRGTVDSLDVIPPQDNSVPPRAGFSHRLSHVTMLSQAAGAVYTLRAPTFSWQHRSAEFNNIIPSSQITQIPLTKSTNLGSGTSVVKGPGFTGGDILRRTSPGQISTLRVNITAPLSQRYRVRIRYASTTNLQFHTSIDGRPINQGNFSATMSSGSNLQSGSFRTVGFTTPFNFSNGSSVFTLSAHVFNSGNEVYIDRIEFVPAEVTFEAEYDLERAQKAVNELFTSSNQIGLKTDVTDYHIDQVSNLVECLSDEFCLDEKQELSEKVKHAKRLSDERNLLQDPNFRGINRQLDRGWRGSTDITIQGGDDVFKENYVTLLGTFDECYPTYLYQKIDESKLKAYTRYQLRGYIEDSQDLEIYLIRYNAKHETVNVPGTGSLWPLSAQSPIGKCGEPNRCAPHLEWNPDLDCSCRDGEKCAHHSHHFSLDIDVGCTDLNEDLGVWVIFKIKTQDGHARLGNLEFLEEKPLVGEALARVKRAEKKWRDKREKLEWETNIVYKEAKESVDALFVNSQYDQLQADTNIAMIHAADKRVHSIREAYLPELSVIPGVNAAIFEELEGRIFTAFSLYDARNVIKNGDFNNGLSCWNVKGHVDVEEQNNQRSVLVLPEWEAEVSQEVRVCPGRGYILRVTAYKEGYGEGCVTIHEIENNTDELKFSNCVEEEIYPNNTVTCNDYTVNQEEYGGAYTSRNRGYNEAPSVPADYASVYEEKSYTDGRRENPCEFNRGYRDYTPLPVGYVTKELEYFPETDKVWIEIGETEGTFIVDSVELLLMEE
            """,
        )

    def test_categorize_database(self):

        response = self.client.get(self.categorize_database_url)
        print("response", response.status_code)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'database/category_display_update.html')

        # def test_statistics(self):
        #
        #     response = self.client.get(self.statistics_url)
        #     print("response", response.status_code)
        #
        #     self.assertEquals(response.status_code, 200)
        #     self.assertTemplateUsed(response, 'database/statistics.html')

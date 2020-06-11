from django.urls import reverse, resolve
from django.test import SimpleTestCase, TestCase
from database.views import statistics, categorize_database, database, search_database, add_cart, clear_session_database, remove_cart, cart_value, view_cart, clear_session_user_data, user_data_remove, user_data, download_sequences, download_data, download_single_sequence, download_category, category_form, category_download, protein_detail


class TestUrls(SimpleTestCase):

    def test_statistics_url_is_resolved(self):
        url = reverse('statistics')
        self.assertEquals(resolve(url).func, statistics)

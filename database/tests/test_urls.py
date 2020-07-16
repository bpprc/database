from django.urls import reverse, resolve
from database import views


# statistics, categorize_database, database, search_database, add_cart, clear_session_database, remove_cart, cart_value, view_cart, clear_session_user_data, user_data_remove, user_data, download_sequences, download_data, download_single_sequence, download_category, category_form, category_download, protein_detail


class TestUrls:

    def test_statistics_url(self):
        path = reverse('statistics')
        assert resolve(path).view_name == 'statistics'

    def test_about_page_url(self):
        path = reverse('about_page')
        assert resolve(path).view_name == 'about_page'

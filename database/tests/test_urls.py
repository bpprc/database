from django.urls import reverse, resolve
from database import views


class TestUrls:

    def test_statistics_url(self):
        path = reverse('statistics')
        assert resolve(path).view_name == 'statistics'

    def test_about_page_url(self):
        path = reverse('about_page')
        assert resolve(path).view_name == 'about_page'

    def test_database_url(self):
        path = reverse('database')
        assert resolve(path).view_name == 'database'

    def test_categorize_database(self):
        path = reverse('categorize_database', kwargs={'str': 'category'})
        assert resolve(path).view_name == 'categorize_database'

    def test_search_database_home(self):
        path = reverse('search_database_home')
        assert resolve(path).view_name == 'search_database_home'

    def test_search_database(self):
        path = reverse('search_database')
        assert resolve(path).view_name == 'search_database'

    def test_add_cart(self):
        path = reverse('add_cart')
        assert resolve(path).view_name == 'add_cart'

    def test_remove_cart(self):
        path = reverse('remove_cart', kwargs={'database_id': 1})
        assert resolve(path).view_name == 'remove_cart'

    def test_clear_session_database(self):
        path = reverse('clear_session_database')
        assert resolve(path).view_name == 'clear_session_database'

    def test_view_cart(self):
        path = reverse('view_cart')
        assert resolve(path).view_name == 'view_cart'

    def test_download_sequences(self):
        path = reverse('download_sequences')
        assert resolve(path).view_name == 'download_sequences'

    def test_clear_session_user_data(self):
        path = reverse('clear_session_user_data')
        assert resolve(path).view_name == 'clear_session_user_data'

    def test_user_data(self):
        path = reverse('user_data')
        assert resolve(path).view_name == 'user_data'

    def test_cart_value(self):
        path = reverse('cart_value')
        assert resolve(path).view_name == 'cart_value'

    def test_user_data_remove(self):
        path = reverse('user_data_remove', kwargs={'id': 1})
        assert resolve(path).view_name == 'user_data_remove'

    def test_download_data(self):
        path = reverse('download_data')
        assert resolve(path).view_name == 'download_data'

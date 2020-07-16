from django.urls import reverse, resolve
from bestmatchfinder import views


class TestUrls:

    def test_submit_home(self):
        path = reverse('submit_home')
        assert resolve(path).view_name == 'submit_home'

    def test_submit(self):
        path = reverse('submit')
        assert resolve(path).view_name == 'submit'

    def test_naming_algorithm(self):
        path = reverse('naming_algorithm')
        assert resolve(path).view_name == 'naming_algorithm'

    def test_run_naming_algorithm(self):
        path = reverse('run_naming_algorithm')
        assert resolve(path).view_name == 'run_naming_algorithm'

    def test_run_align(self):
        path = reverse('run_align')
        assert resolve(path).view_name == 'run_align'

    def test_align_results(self):
        path = reverse('align_results')
        assert resolve(path).view_name == 'align_results'

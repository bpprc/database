from django.urls import reverse, resolve
from bestmatchfinder import views


class TestUrls:

    def test_domain_analysis_homepage(self):
        path = reverse('domain_analysis_homepage')
        assert resolve(path).view_name == 'domain_analysis_homepage'

    def test_domain_analysis(self):
        path = reverse('domain_analysis')
        assert resolve(path).view_name == 'domain_analysis'

    def test_dendogram(self):
        path = reverse('dendogram')
        assert resolve(path).view_name == 'dendogram'

    def test_dendogram_homepage(self):
        path = reverse('dendogram_homepage')
        assert resolve(path).view_name == 'dendogram_homepage'

    def test_domain_analysis_homepage(self):
        path = reverse('domain_analysis_homepage')
        assert resolve(path).view_name == 'domain_analysis_homepage'

    def test_domain_analysis(self):
        path = reverse('domain_analysis')
        assert resolve(path).view_name == 'domain_analysis'

    def test_dendogram(self):
        path = reverse('dendogram')
        assert resolve(path).view_name == 'dendogram'

    def test_dendogram_homepage(self):
        path = reverse('dendogram_homepage')
        assert resolve(path).view_name == 'dendogram_homepage'

    def test_dendogram_homepage2(self):
        path = reverse('dendogram_homepage2')
        assert resolve(path).view_name == 'dendogram_homepage2'

    def test_dendogram_celery(self):
        path = reverse('dendogram_celery')
        assert resolve(path).view_name == 'dendogram_celery'

    def test_taskstatus_clustal_celery(self):
        path = reverse('taskstatus_clustal_celery', kwargs={'str': 'task_id'})
        assert resolve(path).view_name == 'taskstatus_clustal_celery'

    def test_celery_task_status_clustal(self):
        path = reverse('celery_task_status_clustal', kwargs={'str': 'task_id'})
        assert resolve(path).view_name == 'celery_task_status_clustal'

    def test_protein_analysis(self):
        path = reverse('protein_analysis')
        assert resolve(path).view_name == 'protein_analysis'

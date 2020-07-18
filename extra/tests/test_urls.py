from django.urls import reverse, resolve
from bestmatchfinder import views


class TestUrls:

    def test_feedback_home(self):
        path = reverse('feedback_home')
        assert resolve(path).view_name == 'feedback_home'

    def test_github_home(self):
        path = reverse('github_home')
        assert resolve(path).view_name == 'github_home'

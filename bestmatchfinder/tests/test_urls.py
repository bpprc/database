from django.urls import resolve, reverse

from bestmatchfinder import views


class TestUrls:
    def test_bestmatchfinder_home(self):
        path = reverse("bestmatchfinder_home")
        assert resolve(path).view_name == "bestmatchfinder_home"

    def test_bestmatchfinder_database(self):
        path = reverse("bestmatchfinder_database")
        assert resolve(path).view_name == "bestmatchfinder_database"

    def test_run_needle_server(self):
        path = reverse("run_needle_server")
        assert resolve(path).view_name == "run_needle_server"

    def test_run_needle_server_celery(self):
        path = reverse("run_needle_server_celery")
        assert resolve(path).view_name == "run_needle_server_celery"

    def test_taskstatus_needle_celery(self):
        path = reverse(
            "taskstatus_needle_celery", kwargs={"str": "task_id"}
        )
        assert resolve(path).view_name == "taskstatus_needle_celery"

    def test_celery_task_status(self):
        path = reverse("celery_task_status", kwargs={"str": "task_id"})
        assert resolve(path).view_name == "celery_task_status"

    def test_bestmatchfinder_database_sequence_run(self):
        path = reverse("bestmatchfinder_database_sequence_run")
        assert (
            resolve(path).view_name
            == "bestmatchfinder_database_sequence_run"
        )

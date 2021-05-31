from django.apps import AppConfig


class DatabaseConfig(AppConfig):
    name = "database"

    def ready(self):
        import database.signals

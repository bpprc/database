from .settings import *

if os.environ.get("DATABASE_TYPE") == "sqlite3":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "proteindatabase_test",
            "USER": "suresh",
            "PASSWORD": "pannerselvam123",
            "HOST": "localhost",
            "PORT": "5432",
        }
    }

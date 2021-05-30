import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BPPRC.settings")

celery_app = Celery("BPPRC")
celery_app.config_from_object("django.conf.settings", namespace="CELERY")

# here is the beat schedule dictionary defined
celery_app.conf.beat_schedule = {
    "print-every-minute": {
        "task": "namingalgorithm.tasks.run",
        # "schedule": crontab(hour="*/1")
        "schedule": crontab(hour="23", minute="58")
        # 'args': ('Its Thursday!',)
    },
}

celery_app.conf.timezone = "GMT"
celery_app.autodiscover_tasks()

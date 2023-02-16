import os
from celery.schedules import crontab
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tollgator.settings")

app = Celery("tollgator")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")


# Celery Beat Settings
# Define a periodic task to update exchange rates for all currencies
app.conf.beat_schedule = {
    "update-exchange-rates": {
        "task": "common.tasks.update_exchange_rates",
        "schedule": crontab(hour="0, 8, 16", minute=0),
        #'args': (2,)
    }
}


# Load task modules from all registered Django apps.
app.autodiscover_tasks()

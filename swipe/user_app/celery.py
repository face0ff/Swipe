import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swipe.settings")
app = Celery('swipe', backend='redis')
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
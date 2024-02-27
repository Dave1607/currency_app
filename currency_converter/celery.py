from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'currency_converter.settings')

app = Celery('currency_converter')

app.config_from_object('django.conf:settings', namespace='CELERY')

# app.autodiscover_tasks()
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

# Set up Celery logging
logging.basicConfig(level=logging.DEBUG)
from __future__ import absolute_import
from celery import Celery, task
import os
import django
import datetime
django.setup()
from django.apps import apps
from targets.models import Target


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'target.settings')
app = Celery('target')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@task()
def delete_one_week_old_targets():
    delete_date = datetime.date.today() - datetime.timedelta(days=7)
    to_delete = Target.objects.filter(creation_date__lte=delete_date)
    to_delete.delete()

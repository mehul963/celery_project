import os

from celery import Celery
from django.conf import settings
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_config.settings')

app = Celery('admin_config')

# app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.enable_utc=False
app.conf.update(timezone="Asia/Kolkata")

app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()
@app.task(bind=True,ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

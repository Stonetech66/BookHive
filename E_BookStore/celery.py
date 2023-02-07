import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'E_Bookstore.settings')

app=Celery('E_Bookstore')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
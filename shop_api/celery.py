import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_api.settings')

app = Celery('shop_api')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "send_hourly_greetings": {
        "task": "users.tasks.send_hourly_greetings",
        "schedule": crontab(minute=0),  # запуск каждый час в 00 минут
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
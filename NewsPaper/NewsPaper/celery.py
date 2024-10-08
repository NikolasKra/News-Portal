import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')
 
app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'email_news_every_monday_8_utra': {
        'task': 'news.tasks.weekly_post',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        
    },
}
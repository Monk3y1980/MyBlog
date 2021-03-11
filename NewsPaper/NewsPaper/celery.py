import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
# Использование строки здесь означает, что исполнителю не нужно сериализовать
# объект конфигурации для дочерних процессов.
# - namespace = 'CELERY' означает все ключи конфигурации, связанны с ним
# должен иметь префикс CELERY_.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Загружать модули задач из всех зарегистрированных конфигураций приложений Django.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'news.tasks.send_newsletter',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}
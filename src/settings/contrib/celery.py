from celery.schedules import crontab
from celery.signals import worker_ready

from ..django import TIME_ZONE as DJANGO_TIME_ZONE
from ..environment import env

CELERY_TASK_ALWAYS_EAGER = env.bool("SRC_CELERY_TASK_ALWAYS_EAGER", default=False)
CELERY_BROKER_URL = env.str("SRC_CELERY_BROKER", default="redis://redis:6379/1")

CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = DJANGO_TIME_ZONE

CELERYBEAT_SCHEDULE = {
    "update_currency_task": {"task": "flights.update_currency_task", "schedule": crontab(minute=00, hour=12)},
}


@worker_ready.connect
def updated_currency_at_start(sender, **kwargs):
    with sender.app.connection() as conn:
        sender.app.send_task('flights.update_currency_task', connection=conn)

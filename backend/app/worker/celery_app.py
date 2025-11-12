from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.autodiscover_tasks(packages=["app.worker"])

celery_app.conf.beat_schedule = {
    "buscar-dados-onibus-a-cada-minuto": {
        'task': 'app.worker.tasks.task_buscar_dados_onibus',
        "schedule": crontab(), # ou crontab(minute='*/1')
    },
    "verificar-alertas-onibus-a-cada-minuto": {
        'task': 'app.worker.tasks.task_verificar_alertas',
        "schedule": crontab(),
    },
}
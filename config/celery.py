import os

from celery import Celery, signals

from kombu import Queue, Exchange

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config', include=['apps.salon.tasks'])

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.broker_transport_options = {'visibility_timeout': 86400}

app.conf.task_queues = (
    Queue('main', Exchange('main'), routing_key='main'),
)

app.conf.task_routes = {
    'send_push_notifications': {
        'queue': 'main',
    },
}

@signals.setup_logging.connect
def on_celery_setup_logging(**kwargs):
    pass


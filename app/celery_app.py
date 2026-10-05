from celery import Celery

celery_app = Celery("media processor", broker="amqp://guest:guest@rabbitmq:5672//", include=["app.tasks"])

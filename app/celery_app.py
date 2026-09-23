from celery import Celery

celery_app = Celery("media processor", broker="amqp://guest:guest@localhost:5672//", include=["app.tasks"])

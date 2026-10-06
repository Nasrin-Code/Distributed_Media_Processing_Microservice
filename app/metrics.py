from prometheus_client import Gauge
import psutil
from celery import Celery

queue_length = Gauge("queue_length", "Number of jobs waiting in the queue")

worker_cpu_usage = Gauge("worker_cpu_usage", "CPU usage percentage of the worker")

celery_app = Celery(
    "metrics",
    broker="amqp://guest:guest@rabbitmq:5672//",
)

def update_queue_length():
    with celery_app.connection_or_acquire() as connection:
        channel = connection.default_channel
        queue = channel.queue_declare(queue="celery", passive=True)
        queue_length.set(queue.message_count)

def update_worker_cpu():
    cpu_usage = psutil.cpu_percent(interval=1)
    worker_cpu_usage.set(cpu_usage)
    return cpu_usage
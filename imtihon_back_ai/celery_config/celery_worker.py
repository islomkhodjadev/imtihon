# celery_config/celery_worker.py

from celery import Celery

celery_app = Celery(
    "imtihon_tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)

celery_app.conf.update(
    task_serializer="pickle",
    result_serializer="pickle",
    accept_content=["pickle"],  # 👈 This is the key line
)

celery_app.autodiscover_tasks(["celery_config"])

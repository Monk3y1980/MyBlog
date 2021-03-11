# Это гарантирует, что приложение всегда импортируется, когда
# Django запускается, поэтому shared_task будет использовать это приложение.
from .celery import app as celery_app

__all__ = ('celery_app',)
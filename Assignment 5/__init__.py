# from .runner import app

from celery import Celery

# Create a Celery app instance
app = Celery('CIDM6330')

celery = app  # This will now refer to the Celery app instance created later

# Configure Celery using Django's settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks from installed apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

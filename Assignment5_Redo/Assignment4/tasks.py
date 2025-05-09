from celery import shared_task
import time

@shared_task
def add(x, y):
    time.sleep(5) 
    return x + y

@shared_task
def send_email_notification(user_id, subject, message):
    from django.contrib.auth.models import User
    user = User.objects.get(id=user_id)
    print(f"Sending email to {user.email}: {subject} - {message}")

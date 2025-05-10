from django.urls import path
from .views import set_goal_for_client, client_input_goal
from celery import shared_task
from django.utils import time
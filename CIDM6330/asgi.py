import os
from django.core.asgi import get_asgi_application

# Set the default settings module for the 'asgi' application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CIDM6330.settings')

# Get the ASGI application
application = get_asgi_application()

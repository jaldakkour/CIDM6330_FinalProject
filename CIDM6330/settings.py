# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Add Django REST Framework
    'apis',  # Add your custom app
]

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.4.36']
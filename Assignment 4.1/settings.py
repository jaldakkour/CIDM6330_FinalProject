#Add rest_framework to INSTALLED_APPS
#To initialize REST Framework in your project, go to settings.py, and in INSTALLED_APPS add ‘rest_framework’ at the bottom to create api in python django

# Application definition 
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', ]

# Application definition
 
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'apis',
]

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.4.36']


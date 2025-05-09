import os
import sys

sys.path.append("/workspaces/CIDM6330/Assignment4_Redo/")

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Assignment4.settings")

application = get_wsgi_application()

from .runner import app
from .tasks import add

celery = app # you can omit this line
# if you want to use the app instance directly
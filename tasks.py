from celery import Celery
import celery

BROKER_URL = "redis://localhost:6379/0"
BACKEND_URL = "redis://localhost:6379/1"

app = Celery(
    "tasks",
    broker=BROKER_URL,
    backend=BACKEND_URL,
)

from celery import Celery

app = Celery("tasks", broker="redis://localhost:6379/0")

@app.task
def add(x, y):
    return x + y

@app.task
def add(x, y):
    print(f"Adding {x} + {y}")
    return x + y


@app.task
def multiply(x, y):
    print(f"Multiplying {x} + {y}")    
    return x * y


# To start the Celery worker, run the following command in your terminal:
# celery -A tasks worker --loglevel=info
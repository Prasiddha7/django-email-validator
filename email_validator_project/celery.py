from celery import Celery

app = Celery(
    'email_validator_project',
    broker='redis://localhost:6379/0', 
    backend='redis://localhost:6379/0',
    include=['validator.tasks']
)

app.autodiscover_tasks()

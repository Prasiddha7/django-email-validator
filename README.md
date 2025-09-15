Set Up Instructions
1. Clone repo and setup virtual environment
   git clone https://github.com/Prasiddha7/django_email_validator.git
   cd django_email_validator
   python3 -m venv venv
   source venv/bin/activate

2. Install Dependencies
   pip install -r requirements.txt
   
3. Install and Start Redis (Broker & Backend)
  brew install redis
  brew services start redis

4. Run migrations
  python manage.py migrate

5. Start Django Server
  python manage.py runserver

   
6. Start Celery Worker
  celery -A email_validator_project worker --loglevel=info

API Endpoints
Validate Emails
POST http://127.0.0.1:8000/api/validate/
Check Task Status
GET http://127.0.0.1:8000/api/status/<task_id>/

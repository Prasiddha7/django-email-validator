from django.urls import path
from .views import ValidateEmailsAPIView, task_status

urlpatterns = [
    path('validate/', ValidateEmailsAPIView.as_view(), name='validate_emails'), 
    path('status/<str:task_id>/', task_status, name='task_status'),
]

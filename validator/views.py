
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import EmailValidateSerializer
from .tasks import validate_emails_task
from celery.result import AsyncResult

class ValidateEmailsAPIView(APIView):
    def post(self, request):
        serializer = EmailValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        emails = serializer.validated_data['emails']

        task = validate_emails_task.delay(emails)
        return Response({'task_id': task.id, 'status': 'processing'})
    


@api_view(['GET'])
def task_status(request, task_id):
    result = AsyncResult(task_id)
    if result.ready():
        return Response({'status': 'completed', 'result': result.result})
    else:
        return Response({'status': 'processing'})
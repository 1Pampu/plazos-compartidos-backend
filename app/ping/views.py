from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
import random

@api_view(['GET'])
def RandomNumberView(request):
    random_number = random.randint(1, 100)
    now = timezone.localtime(timezone.now())
    return Response({'random_number': random_number, 'date': now.date(), 'time': now.time()})
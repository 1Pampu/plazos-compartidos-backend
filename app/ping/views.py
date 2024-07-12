from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
import random

@api_view(['GET'])
def RandomNumberView(request):
    random_number = random.randint(1, 100)
    return Response({'random_number': random_number, 'date': timezone.now().date(), 'time': timezone.now().time()})
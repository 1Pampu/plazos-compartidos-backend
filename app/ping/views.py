from rest_framework.decorators import api_view
from rest_framework.response import Response
import random

@api_view(['GET'])
def RandomNumberView(request):
    random_number = random.randint(1, 100)
    return Response({'random_number': random_number})
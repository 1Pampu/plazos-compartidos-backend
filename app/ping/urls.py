from django.urls import path
from .views import RandomNumberView

urlpatterns = [
    path('ping', RandomNumberView),
]
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from app.users.manager import MyUserManager
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True, db_index=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
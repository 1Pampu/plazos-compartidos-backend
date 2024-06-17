from rest_framework import serializers, exceptions, serializers
from django.contrib.auth import authenticate
from .models import User

# Create your serializers here.
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'username', 'tokens']

    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=255, min_length=3, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj) -> dict:

        user: User = User.objects.get(email=obj['email'])
        return {
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh'],
        }

    def validate(self, attrs) -> dict:
        email: str = attrs.get('email', '')
        password: str = attrs.get('password', '')

        user = authenticate(email=email, password=password)
        if not user:
            raise exceptions.AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise exceptions.AuthenticationFailed('Account disables, contact admin')

        return {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type'}, min_length=4, max_length=12, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self) -> None:
        user: User = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password: str = self.validated_data['password']
        password2: str = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})

        user.set_password(password)
        user.save()
        return user
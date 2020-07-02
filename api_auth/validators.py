from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from rest_framework_simplejwt import exceptions
from django.contrib.auth import get_user_model

from api_auth.models import Auth

User = get_user_model()


class AuthenticationValidator:
    requires_context = True

    def __call__(self, value, serializer_field):
        email = serializer_field.initial_data.get('email')
        if not email:
            raise serializers.ValidationError('email field required')
        confirmation_code = serializer_field.initial_data.get('confirmation_code')
        if not confirmation_code:
            raise serializers.ValidationError('confirmation_code field required')

        credentials = Auth.objects.filter(email=email)
        if not credentials.exists() or not credentials[0].check_confirmation_code(confirmation_code):
            raise exceptions.AuthenticationFailed()

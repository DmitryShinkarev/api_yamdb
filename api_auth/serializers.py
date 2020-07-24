from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from rest_framework import serializers

from api_auth.models import Auth
from api_auth.validators import AuthenticationValidator

User = get_user_model()


class AuthenticationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ('email', 'confirmation_code')
        read_only_fields = ('email', 'confirmation_code')
        model = Auth
        validators = [AuthenticationValidator(), ]


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('email',)
        read_only_fields = ('user',)
        model = Auth

    def create(self, validated_data):
        email = validated_data.get('email')
        username = email.split('@')[0]
        users = User.objects.filter(email=email, username=username)
        if not users.exists():
            user = User.objects.create(email=email, username=username)
        else:
            user = users[0]

        credentials = Auth(email=email, user=user)
        raw_confirmation_code = get_random_string()
        credentials.set_confirmation_code(raw_confirmation_code)
        credentials.save()
        credentials.send_email(email, raw_confirmation_code)
        return credentials

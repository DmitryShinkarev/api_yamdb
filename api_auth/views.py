from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt import exceptions
from rest_framework_simplejwt.tokens import RefreshToken

from api_auth.serializers import AuthenticationSerializer, RegistrationSerializer

User = get_user_model()


class RegisterUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = RegistrationSerializer

    def perform_create(self, serializer):
        email = serializer.validated_data['email']
        user = get_object_or_404(User, email=email)
        serializer.save(user=user)


class ObtainTokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = AuthenticationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        users = User.objects.filter(email=request.data['email'])

        if not users.exists():
            raise exceptions.AuthenticationFailed()

        refresh = RefreshToken.for_user(users[0])
        return Response({'token': str(refresh.access_token)}, status=status.HTTP_200_OK)

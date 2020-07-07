from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api_users.permissions import IsOwnProfileOrAdmin
from api_users.serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnProfileOrAdmin,)
    pagination_class = PageNumberPagination
    search_fields = ('=username',)
    lookup_field = 'username'

    def create(self, request, *args, **kwargs):
        if self.kwargs.get('username') == 'me':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().create(request, args, kwargs)

    def retrieve(self, request, *args, **kwargs):
        if self.kwargs.get('username') == 'me':
            self.kwargs['username'] = request.user.username
        return super().retrieve(request, args, kwargs)

    def partial_update(self, request, *args, **kwargs):
        if self.kwargs.get('username') == 'me':
            self.kwargs['username'] = request.user.username
        return super().partial_update(request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        if self.kwargs.get('username') == 'me':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, args, kwargs)

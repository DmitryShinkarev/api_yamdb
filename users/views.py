from django.shortcuts import render

from .serializers import *
from .models import User
from rest_framework.response import Response

from .permissions import IsAdmin
from .serializers import UserSerializer

from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    model = User
    serializer = UserSerializer

def AnyUser(request, username):
    user = get_object_or_404(User, username=username)
    return user

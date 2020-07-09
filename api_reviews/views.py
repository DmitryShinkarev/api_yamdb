from django.shortcuts import render

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, status, permissions
from rest_framework.pagination import PageNumberPagination

from api_titles.models import Title
from .permissions import IsOwnProfileOrAdmin
from .filters import 

# Create your views here.
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerialier
    permission_classes = (IsOwnProfileOrAdmin)
    pagination_class = PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        if Review.objects.filter(title=title, author=self.request.user).exists():
            raise ParseError
        serializer.save(author=self.request.user, title=title)
        int_rating = Review.objects.filter(title=title).aggregate(Avg('score'))
        title.rating = int_rating['score__avg']
        title.save(update_fields=["rating"])

    def perform_update(self, serializer):
        serializer.save()
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        int_rating = Review.objects.filter(title=title).aggregate(Avg('score'))
        title.rating = int_rating['score__avg']
        title.save(update_fields=["rating"])
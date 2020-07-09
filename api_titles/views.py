from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters, status
from rest_framework.exceptions import ParseError
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api_titles.filters import TitleFilter
from api_titles.models import Category, Genre, Title, Review
from api_titles.permissions import IsAdminOrReadOnly
from api_titles.serializers import CategorySerializer, GenreSerializer, TitleSerializer, ReviewSerializer


class CategoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class GenreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        genre = Genre.objects.filter(slug__in=self.request.data.getlist('genre'))
        category = get_object_or_404(Category, slug=self.request.data.get('category'))
        serializer.save(genre=genre, category=category, rating=None)

    def perform_update(self, serializer):
        genre = Genre.objects.filter(slug__in=self.request.data.getlist('genre'))
        category = get_object_or_404(Category, slug=self.request.data.get('category'))
        serializer.save(genre=genre, category=category)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
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

    def partial_update(self, request, *args, **kwargs):
        review = get_object_or_404(Review, pk=self.kwargs.get('pk'))
        user = request.user
        if review.author != user and user.role != 'admin' and user.role != 'moderator':
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        role = request.user.role
        if role != 'admin' and role != 'moderator':
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, args, kwargs)

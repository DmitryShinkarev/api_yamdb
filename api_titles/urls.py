from rest_framework.routers import DefaultRouter

from api_titles.views import CategoryViewSet, GenreViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)

from rest_framework.routers import SimpleRouter
from django.urls import path, include
from api.views import (CategoryViewSet, GenreViewSet,
                       TitleViewSet)


router = SimpleRouter()

router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router.urls)),
]

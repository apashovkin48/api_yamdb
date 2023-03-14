from rest_framework.routers import SimpleRouter
from django.urls import path, include
from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, SignUpViewSet, TitleViewSet, TokenView,
                       UserViewSet, get_profile)


router = SimpleRouter()

router.register('users', UserViewSet, basename='users')
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register('titles', TitleViewSet, basename='titles')

router.register(
    'posts',
    PostViewSet,
    basename='posts'
)


urlpatterns = [
    path('v1/', include(router.urls)),
]

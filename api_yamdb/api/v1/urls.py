from api import views
from django.urls import path, include
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('users', views.UserViewSet, basename='users')
router.register('genres', views.GenreViewSet, basename='genres')
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('titles', views.TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    views.CommentViewSet,
    basename='comments'
)
urlpatterns_auth = [
    path('signup/', views.api_signup),
    path('token/', views.api_token)
]

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include(urlpatterns_auth)),
]

from rest_framework.routers import SimpleRouter
from django.urls import path, include
from . import views
from rest_framework import routers


router = SimpleRouter()
router.register('users',views.UserViewSet,basename='users')
router.register('genres', views.GenreViewSet, basename='genres')
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('titles', views.TitleViewSet, basename='titles')

# for test viewsets
router.register(
    'reviews',
    views.ReviewViewSet,
    basename='reviews'
)
router.register(
    r'reviews/(?P<review_id>[\d]+)/comments',
    views.CommentViewSet,
    basename='comments'
)

# wait title model
"""
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
    basename='comments'
)
"""

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', views.api_signup),
    path('v1/auth/token/', views.api_token)
]

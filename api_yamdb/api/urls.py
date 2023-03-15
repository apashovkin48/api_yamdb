from rest_framework.routers import SimpleRouter
from django.urls import path, include
from api.views import ReviewViewSet, CommentViewSet
from . import views

router = SimpleRouter()

# for test viewsets
router.register(
    'reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
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
path('v1/auth/signup/',views.api_signup),
path('v1/auth/token/',views.api_token)
]

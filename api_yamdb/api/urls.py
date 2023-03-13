from rest_framework.routers import SimpleRouter
from django.urls import path, include

router = SimpleRouter()
# exmaple
"""
router.register(
    'posts',
    PostViewSet,
    basename='posts'
)
"""

urlpatterns = [
    path('v1/', include(router.urls)),
]

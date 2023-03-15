from . import views
from django.urls import path, include
from rest_framework import routers


v1_router = routers.DefaultRouter()
v1_router.register('users',views.UserViewSet,basename='users')

urlpatterns = [
path('v1/', include(v1_router.urls)),
path('v1/auth/signup/',views.api_signup),
path('v1/auth/token/',views.api_token)
]

from django.urls import path
from . import views

urlpatterns = [
path('v1/auth/signup/',views.api_signup),
path('v1/auth/token/',views.api_token)
]

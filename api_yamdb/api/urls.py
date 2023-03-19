from django.urls import path, include
from . import views
from .v1 import urls as v1_urls


urlpatterns = [
    path('v1/', include(v1_urls.router.urls)),
    path('v1/auth/signup/', views.api_signup),
    path('v1/auth/token/', views.api_token)
]

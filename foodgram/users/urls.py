from django.urls import include, path
from rest_framework import routers

from .views import UserCustomViewSet

app_name = 'users'

router = routers.DefaultRouter()

router.register(r'users', UserCustomViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]

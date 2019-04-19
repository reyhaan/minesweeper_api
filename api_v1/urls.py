from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register('map', views.MapViewSet, base_name='map')

urlpatterns = [
    path(r'', include(router.urls))
]
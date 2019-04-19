from django.urls import path, include
from . import views

urlpatterns = [
    path('game/', views.GameView.as_view())
]
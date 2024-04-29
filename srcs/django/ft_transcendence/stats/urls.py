from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_stats, name='user_stats'),
]
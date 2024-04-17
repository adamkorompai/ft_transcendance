from django.urls import path
from . import views

urlpatterns = [
    path('pong', views.pong_game, name='pong_game'),
    path('', views.play, name='play'),
    path('quick_play', views.quick_play, name='quick_play'),
]
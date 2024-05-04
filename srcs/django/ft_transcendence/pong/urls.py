from django.urls import path
from . import views

urlpatterns = [
    path('pong', views.pong_game, name='pong_game'),
    path('', views.play, name='play'),
    path('quick_play', views.quick_play, name='quick_play'),
    path('tournaments', views.tournaments, name='tournaments'),
    path('create-tournament/', views.create_tournament, name='create_tournament'),
    path('tree/<int:tournament_id>/', views.tree, name="tree"),
    path('start_game/<int:match_id>/', views.start_game, name='start_game'),
    path('record_game_winner/<int:match_id>/', views.record_game_winner, name='record_game_winner'),
    path('end-tournament/<int:tournament_id>/', views.end_tournament, name='end_tournament'),
    path('check-user/<str:username>/', views.check_user, name='check_user'),
    path('save-game-stats/', views.save_game_stats, name='save_game_stats'),
]
from django.urls import path
from . import views

urlpatterns = [
    # path('pong', views.pong_game, name='pong_game'),
    path('pong/', views.pong_game, name='pong_game'),
    path('pong_ia/', views.pong_ia_game, name='pong_ia_game'),
    path('', views.play, name='play'),
    path('quick_play', views.quick_play, name='quick_play'),
    path('tournaments', views.tournaments, name='tournaments'),
    path('check-user/<str:username>/', views.check_user, name='check_user'),
    path('save-game-stats/', views.save_game_stats, name='save_game_stats'),
    path('save-ia-game-stats/', views.save_ia_game_stats, name='save_ia_game_stats'),
    path('search-opponents/', views.search_opponents, name='search_opponents'),
    path('tournaments/', views.tournaments, name='tournaments'),
    path('tournaments/create/', views.create_tournament, name='create_tournament'),
    path('tournaments/<int:tournament_id>/', views.tournament_detail, name='tournament_detail'),
    path('tournaments/<int:tournament_id>/signup/', views.tournament_signup, name='tournament_signup'),
    path('tournaments/<int:tournament_id>/game/', views.tournament_game, name='tournament_game'),
    path('tournaments/<int:tournament_id>/start/', views.tournament_start, name='tournament_start'),
    path('tournaments/<int:tournament_id>/delete/', views.tournament_delete, name='tournament_delete'),
    path('tournaments/<int:tournament_id>/submit-match-result/', views.submit_match_result, name='submit_match_result'),
    path('tournaments/<int:tournament_id>/next-match/', views.get_next_match, name='get_next_match'),
]
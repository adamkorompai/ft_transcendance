import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ft_transcendence.settings')
django.setup()

from django.contrib.auth.models import User
from stats.models import UserStats

users = User.objects.all()
for user in users:
    total_games = random.randint(10, 100)
    wins = random.randint(0, total_games)
    losses = total_games - wins
    goals_scored = random.randint(0, 200)
    goals_conceded = random.randint(0, 100)
    time_played = random.randint(1, 60)  # Entre 1 min et 1 heures
    nb_defense = random.randint(0, 150)
    
    # Récup l'instance UserStats pour l'user
    user_stats, created = UserStats.objects.get_or_create(user=user)
    
    # MAJ les champs de l'instance UserStats avec datas
    user_stats.total_games = total_games
    user_stats.wins = wins
    user_stats.losses = losses
    user_stats.goals_scored = goals_scored
    user_stats.goals_conceded = goals_conceded
    user_stats.time_played = time_played
    user_stats.nb_defense = nb_defense
    
    # historique des matchs
    match_history = []
    for _ in range(total_games):
        opponent = random.choice(users)
        while opponent == user:
            opponent = random.choice(users)
        
        user_score = random.randint(0, 10)
        opponent_score = random.randint(0, 10)
        
        match_data = {
            'opponent': opponent.username,
            'user_score': user_score,
            'opponent_score': opponent_score
        }
        match_history.append(match_data)
    
    user_stats.match_history = match_history

    user_stats.save()

print("Statistiques des utilisateurs mises à jour avec succès.")
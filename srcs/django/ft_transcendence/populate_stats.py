import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ft_transcendence.settings')
django.setup()

from django.contrib.auth.models import User
from stats.models import UserStats

# Supprime toutes les instances de UserStats
UserStats.objects.all().delete()

users = User.objects.all()
for user in users:
    total_games = random.randint(10, 100)
    wins = random.randint(0, total_games)
    losses = total_games - wins
    goals_scored = random.randint(0, 200)
    goals_conceded = random.randint(0, 100)
    time_played = random.randint(60, 600)  # Entre 1 heure et 10 heures
    nb_defense = random.randint(0, 150)
    
    # Générer l'historique des matchs pour chaque utilisateur
    match_history = []
    for _ in range(total_games):
        opponent = random.choice(users)
        while opponent == user:
            opponent = random.choice(users)
        
        user_score = random.randint(0, 9)
        opponent_score = random.randint(0, 9)
        
        match_data = {
            'opponent': opponent.username,
            'user_score': user_score,
            'opponent_score': opponent_score
        }
        match_history.append(match_data)
    
    UserStats.objects.create(
        user=user,
        total_games=total_games,
        wins=wins,
        losses=losses,
        goals_scored=goals_scored,
        goals_conceded=goals_conceded,
        time_played=time_played,
        nb_defense=nb_defense,
        match_history=match_history
    )

print("Statistiques des utilisateurs générées avec succès.")
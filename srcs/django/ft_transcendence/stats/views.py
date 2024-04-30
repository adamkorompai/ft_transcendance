from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserStats
from django.db.models import F

@login_required
def user_stats(request):
    user = request.user
    stats, created = UserStats.objects.get_or_create(user=user)

    # Calcul des ratios
    if stats.total_games > 0:
        stats.win_ratio = round(stats.wins / stats.total_games * 100, 2)
        stats.loss_ratio = round(stats.losses / stats.total_games * 100, 2)
        
        total_goals = stats.goals_scored + stats.goals_conceded
        if total_goals > 0:
            stats.goals_scored_ratio = round(stats.goals_scored / total_goals * 100, 2)
            stats.goals_conceded_ratio = round(stats.goals_conceded / total_goals * 100, 2)
        else:
            stats.goals_scored_ratio = 0
            stats.goals_conceded_ratio = 0
        
        total_defense_conceded = stats.nb_defense + stats.goals_conceded
        if total_defense_conceded > 0:
            stats.defense_ratio = round(stats.nb_defense / total_defense_conceded * 100, 2)
            stats.conceded_ratio = round(stats.goals_conceded / total_defense_conceded * 100, 2)
        else:
            stats.defense_ratio = 0
            stats.conceded_ratio = 0
        
        total_defense_scored = stats.nb_defense + stats.goals_scored
        if total_defense_scored > 0:
            stats.defense_scored_ratio = round(stats.nb_defense / total_defense_scored * 100, 2)
            stats.scored_ratio = round(stats.goals_scored / total_defense_scored * 100, 2)
        else:
            stats.defense_scored_ratio = 0
            stats.scored_ratio = 0
        stats.nb_defense_ratio = round(stats.nb_defense / stats.total_games, 2)
        stats.time_played_ratio = round(stats.time_played / stats.total_games, 2)
    else:
        stats.win_ratio = 0
        stats.loss_ratio = 0
        stats.goals_scored_ratio = 0
        stats.goals_conceded_ratio = 0
        stats.defense_ratio = 0
        stats.conceded_ratio = 0
        stats.defense_scored_ratio = 0
        stats.scored_ratio = 0
        stats.nb_defense_ratio = 0
        stats.time_played_ratio = 0

    # Récup les 3 meilleurs utilisateurs par wins, total games et ratio de victoires
    top_by_wins = UserStats.objects.order_by('-wins')[:3]
    top_by_total_games = UserStats.objects.order_by('-total_games')[:3]
    top_by_win_ratio = UserStats.objects.filter(total_games__gt=0).annotate(
        win_ratio=F('wins') * 100 / F('total_games')
    ).order_by('-win_ratio')[:3]

    context = {
        'stats': stats,
        'top_by_wins': top_by_wins,
        'top_by_total_games': top_by_total_games,
        'top_by_win_ratio': top_by_win_ratio,
    }
    return render(request, 'stats/user_stats.html', context)
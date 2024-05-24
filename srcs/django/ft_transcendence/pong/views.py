from django.shortcuts import render, redirect
from render_block import render_block_to_string
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Tournament, TournamentMatch, Announcement
import random, math
from django.urls import reverse
from math import ceil, log2
from django.db.models import Max
from django.templatetags.static import static
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from stats.models import UserStats
import json

# Create your views here.
def pong_game(request):
    if request.method == 'POST':
        player1_username = request.POST.get('player1')
        player2_username = request.POST.get('player2')
        
        player1 = get_object_or_404(User, username=player1_username)
        player1_stats, _ = UserStats.objects.get_or_create(user=player1)
        
        if player2_username:
            player2 = get_object_or_404(User, username=player2_username)
            player2_stats, _ = UserStats.objects.get_or_create(user=player2)
        else:
            player2_stats = None
        
        context = {
            'player1_stats': player1_stats,
            'player2_stats': player2_stats,
            'player1_username': player1_username,
            'player2_username': player2_username,
        }
        
        return render(request, 'game.html', context)
    
    return redirect('quick_play')

def pong_ia_game(request):
    if request.method == 'POST':
        player1_username = request.POST.get('player1')
        player1 = get_object_or_404(User, username=player1_username)
        player1_stats, _ = UserStats.objects.get_or_create(user=player1)
        context = {
            'player1_stats': player1_stats,
            'player1_username': player1_username,
        }
        return render(request, 'game_ia.html', context)
    return redirect('quick_play')

def play(request):
    if 'HTTP_HX_REQUEST' in request.META:
        context = {"request": request}
        html = render_block_to_string('play.html', 'body', context)
        return HttpResponse(html)
    return render(request, 'play.html')

def quick_play(request):
    if 'HTTP_HX_REQUEST' in request.META:
        context = {"request": request}
        html = render_block_to_string('quickplay.html', 'body', context)
        return HttpResponse(html)
    return render(request, 'quickplay.html')

def tournaments(request):
    """
    View to display tournaments.
    """
    last_tournament = Tournament.objects.last()
    if last_tournament and not last_tournament.is_finished:
        return redirect('tree', tournament_id=last_tournament.id)
    users = User.objects.all()
    context = {"users": users}
    return render(request, 'tournaments.html', context)

def create_tournament(request):
    """
    View to create a new tournament.
    """
    if request.method == 'POST':
        nb_players = int(request.POST.get('nb_players'))
        player_ids = request.POST.getlist('players')

        tournament = Tournament.objects.create(nb_players=nb_players)

        # Create first round matches
        if nb_players >= 2:
            # Assuming the players are selected randomly, you can implement your own logic here
            selected_players = player_ids[:nb_players]
            for i in range(0, nb_players, 2):
                match = TournamentMatch.objects.create(
                    tournament=tournament,
                    participant1_id=selected_players[i],
                    participant2_id=selected_players[i + 1]
                )

        return redirect('tree', tournament_id=tournament.id)
    else:
        users = User.objects.all()
        context = {'users': users}
        return render(request, 'create_tournament.html', context)

def tree(request, tournament_id):
    """
    View to display the tournament tree.
    """
    try:
        tournament = Tournament.objects.get(pk=tournament_id)
        matches = TournamentMatch.objects.filter(tournament=tournament)
        nb_players = tournament.nb_players

        # Determine the template name based on the number of players
        if nb_players == 4:
            template_name = 'tree_4.html'
        elif nb_players == 8:
            template_name = 'tree_8.html'
        elif nb_players == 16:
            template_name = 'tree_16.html'

        try:
            announcement = Announcement.objects.latest('timestamp')
        except Announcement.DoesNotExist:
            announcement = None

    except Tournament.DoesNotExist:
        tournament = None
        matches = None
        announcement = None

    return render(request, template_name, {'tournament': tournament, 'matches': matches, 'announcement': announcement})

def start_game(request, match_id):
    match = TournamentMatch.objects.get(id=match_id)
    return render(request, 'tmp.html', {'match': match})

def record_game_winner(request, match_id):
    if request.method == 'POST':
        match = TournamentMatch.objects.get(id=match_id)
        winner_id = request.POST.get('winner')
        winner = User.objects.get(id=winner_id)
        match.winner = winner
        match.save()
        announcement_content = f"The next match is ready to play! {winner} just won his match !"
        Announcement.objects.create(title="Next Match Ready", content=announcement_content)

        tournament = match.tournament
        next_round = match.round_number + 1
        
        # Check if all matches in this round have winners
        if not TournamentMatch.objects.filter(tournament=tournament, round_number=match.round_number, winner=None).exists():
            # Check if it's the final round
            if next_round * 2 <= tournament.nb_players:
                # Generate matches for the next round
                generate_next_round_matches(tournament)
            else:
                # Tournament finished
                tournament.is_finished = True
                tournament.save()
                Announcement.objects.create(title="Tournament Finished", content="The tournament is finished!")

    return redirect('tree', tournament_id=match.tournament_id)

def generate_next_round_matches(tournament):
    # Get the maximum round number played so far in the tournament
    max_round_number = TournamentMatch.objects.filter(tournament=tournament).aggregate(Max('round_number'))['round_number__max'] or 0
    
    # Increment the round number for the next round
    next_round_number = max_round_number + 1
    
    # Retrieve the winners of the current round
    winners = TournamentMatch.objects.filter(tournament=tournament, winner__isnull=False, round_number=max_round_number)
    
    # Create matches for the next round using the winners of the current round
    for i in range(0, len(winners), 2):

        if i + 1 < len(winners):
            participant1 = winners[i].winner
            participant2 = winners[i + 1].winner

            # Create a match between the winners if it doesn't already exist
            if not TournamentMatch.objects.filter(tournament=tournament, participant1=participant1, participant2=participant2).exists():
                TournamentMatch.objects.create(
                    tournament=tournament,
                    participant1=participant1,
                    participant2=participant2,
                    round_number=next_round_number
                )

def end_tournament(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    tournament.is_finished = True
    tournament.save()
    Announcement.objects.all().delete()
    return redirect('play')

def check_user(request, username):
    try:
        user = User.objects.get(username=username)
        profile_image = user.profile.image.url
        return JsonResponse({'exists': True, 'profile_image': profile_image})
    except User.DoesNotExist:
        default_image = static('../media/default.png')
        return JsonResponse({'exists': False, 'profile_image': default_image})

def save_game_stats(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        player1_username = data['player1']
        player2_username = data['player2']
        player1_score = data['player1_score']
        player2_score = data['player2_score']
        time_played = data['time_played']
        player1_nb_defense = data['player1_nb_defense']
        player2_nb_defense = data['player2_nb_defense']

        player1 = User.objects.get(username=player1_username)
        player1_stats, _ = UserStats.objects.get_or_create(user=player1)
        player1_stats.total_games += 1
        player1_stats.goals_scored += player1_score
        player1_stats.goals_conceded += player2_score
        player1_stats.time_played += time_played
        player1_stats.nb_defense += player1_nb_defense

        if player1_score > player2_score:
            player1_stats.wins += 1
        else:
            player1_stats.losses += 1

        if player2_username:
            player2 = User.objects.get(username=player2_username)
            player2_profile_image = player2.profile.image.url
        else:
            player2_profile_image = None

        match_data = {
            'opponent': player2_username,
            'user_score': player1_score,
            'opponent_score': player2_score,
            'opponent_profile_image': player2_profile_image
        }
        player1_stats.match_history.append(match_data)
        player1_stats.save()

        if player2_username:
            player2_stats, _ = UserStats.objects.get_or_create(user=player2)
            player2_stats.total_games += 1
            player2_stats.goals_scored += player2_score
            player2_stats.goals_conceded += player1_score
            player2_stats.time_played += time_played
            player2_stats.nb_defense += player2_nb_defense

            if player2_score > player1_score:
                player2_stats.wins += 1
            else:
                player2_stats.losses += 1

            player1_profile_image = player1.profile.image.url

            match_data_player2 = {
                'opponent': player1_username,
                'user_score': player2_score,
                'opponent_score': player1_score,
                'opponent_profile_image': player1_profile_image
            }
            player2_stats.match_history.append(match_data_player2)
            player2_stats.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})

def save_ia_game_stats(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        player_username = data.get('player')
        if player_username is None:
            return JsonResponse({'status': 'error', 'message': 'Player username is missing'})
        
        player_score = data.get('player_score', 0)
        ia_score = data.get('ia_score', 0)
        time_played = data.get('time_played', 0)
        player_nb_defense = data.get('player_nb_defense', 0)

        player = User.objects.get(username=player_username)
        player_stats, _ = UserStats.objects.get_or_create(user=player)

        player_stats.total_games += 1
        player_stats.goals_scored += player_score
        player_stats.goals_conceded += ia_score
        player_stats.time_played += time_played
        player_stats.nb_defense += player_nb_defense

        if player_score > ia_score:
            player_stats.wins += 1
        else:
            player_stats.losses += 1

        match_data = {
            'opponent': 'Pong GPT',
            'user_score': player_score,
            'opponent_score': ia_score
        }
        player_stats.match_history.append(match_data)

        player_stats.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})

def search_opponents(request):
    query = request.GET.get('query', '')
    opponents = User.objects.filter(username__istartswith=query)
    data = [{'username': opponent.username} for opponent in opponents]
    return JsonResponse(data, safe=False)
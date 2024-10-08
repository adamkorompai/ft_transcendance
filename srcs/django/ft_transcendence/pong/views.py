from django.shortcuts import render, redirect, get_object_or_404
from render_block import render_block_to_string
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
import random, math
from django.urls import reverse
from math import ceil, log2
from django.db.models import Max
from django.templatetags.static import static
from stats.models import UserStats
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Tournament, TournamentParticipant, TournamentMatch
from . import views
from datetime import timedelta
from django.utils import timezone

@login_required(login_url='/accounts/login/?redirected=true')
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

@login_required(login_url='/accounts/login/?redirected=true')
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

@login_required(login_url='/accounts/login/?redirected=true')
def play(request):
    if 'HTTP_SPA_CHECK' in request.META:
        context = {"request": request}
        html = render_block_to_string('play.html', 'body', context)
        return HttpResponse(json.dumps({"html": html, "title": "Play"}), content_type="application/json")
    return render(request, 'play.html', {'title': "Play"})

@login_required(login_url='/accounts/login/?redirected=true')
def quick_play(request):
    if 'HTTP_SPA_CHECK' in request.META:
        context = {"request": request}
        html = render_block_to_string('quickplay.html', 'body', context)
        return HttpResponse(json.dumps({"html": html, "title": "Quickplay"}), content_type="application/json")
    return render(request, 'quickplay.html')

@login_required(login_url='/accounts/login/?redirected=true')
def check_user(request, username):
    try:
        user = User.objects.get(username=username)
        profile_image = user.profile.image.url
        return JsonResponse({'exists': True, 'profile_image': profile_image})
    except User.DoesNotExist:
        default_image = static('../media/default.png')
        return JsonResponse({'exists': False, 'profile_image': default_image})

@login_required(login_url='/accounts/login/?redirected=true')
def save_game_stats(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        tournament_id = data['tournament_id']
        
        if tournament_id != 0:
            tournament = get_object_or_404(Tournament, id=tournament_id)
            current_match = tournament.get_current_match()
            
            if current_match:
                winner_username = data['winner']
                winner = User.objects.get(username=winner_username)
                current_match.winner = winner
                current_match.save()
        
        player1_username = data['player1']
        player2_username = data['player2']
        player1_score = data['player1_score']
        player2_score = data['player2_score']
        time_played = data['time_played']
        player1_nb_defense = data['player1_nb_defense']
        player2_nb_defense = data['player2_nb_defense']

        player1 = User.objects.get(username=player1_username)
        player2 = User.objects.get(username=player2_username)

        match_date = timezone.now() + timedelta(hours=2)
        
        player1_stats, _ = UserStats.objects.get_or_create(user=player1)
        player1_stats.total_games += 1
        player1_stats.goals_scored += player1_score
        player1_stats.goals_conceded += player2_score
        player1_stats.time_played += time_played
        player1_stats.nb_defense += player1_nb_defense
        player1_stats.match_history.append({
            'opponent': player2_username,
            'user_score': player1_score,
            'opponent_score': player2_score,
            'opponent_profile_image': player2.profile.image.url,
            'date': match_date.strftime('%d-%m-%Y %H:%M:%S'),
            'defense': player1_nb_defense,
            'game_time': time_played
        })

        if player1_score > player2_score:
            player1_stats.wins += 1
        else:
            player1_stats.losses += 1
        player1_stats.save()

        player2_stats, _ = UserStats.objects.get_or_create(user=player2)
        player2_stats.total_games += 1
        player2_stats.goals_scored += player2_score
        player2_stats.goals_conceded += player1_score
        player2_stats.time_played += time_played
        player2_stats.nb_defense += player2_nb_defense
        player2_stats.match_history.append({
            'opponent': player1_username,
            'user_score': player2_score,
            'opponent_score': player1_score,
            'opponent_profile_image': player1.profile.image.url,
            'date': match_date.strftime('%Y-%m-%d %H:%M:%S'),
            'defense': player2_nb_defense,
            'game_time': time_played
        })

        if player2_score > player1_score:
            player2_stats.wins += 1
        else:
            player2_stats.losses += 1
        player2_stats.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})


@login_required(login_url='/accounts/login/?redirected=true')
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

        match_date = timezone.now() + timedelta(hours=2)

        if player_score > ia_score:
            player_stats.wins += 1
        else:
            player_stats.losses += 1

        match_data = {
            'opponent': 'Pong GPT',
            'user_score': player_score,
            'opponent_score': ia_score,
            'date': match_date.strftime('%d-%m-%Y %H:%M:%S'),
            'defense': player_nb_defense,
            'game_time': time_played

        }
        player_stats.match_history.append(match_data)

        player_stats.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})

@login_required(login_url='/accounts/login/?redirected=true')
def search_opponents(request):
    query = request.GET.get('query', '')
    opponents = User.objects.filter(username__istartswith=query)
    data = [{'username': opponent.username} for opponent in opponents]
    return JsonResponse(data, safe=False)

@login_required(login_url='/accounts/login/?redirected=true')
def tournaments(request):
    tournaments = Tournament.objects.all()
    return render(request, 'tournaments.html', {'tournaments': tournaments})

@login_required(login_url='/accounts/login/?redirected=true')
def create_tournament(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        number_of_players = request.POST.get('number_of_players')
        creator = request.user

        players = User.objects.all()
        for player in players:
            player.profile.alias = ''
            player.profile.save()
        Tournament.objects.create(name=name, number_of_players=number_of_players, creator=creator)
        return redirect('tournaments')

    return render(request, 'tournaments.html')

@login_required(login_url='/accounts/login/?redirected=true')
def tournament_detail(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    participants = tournament.participants.all()
    user_in_tournament = participants.filter(player=request.user).exists()

    if tournament.is_started and tournament.creator != request.user:
        messages.error(request, "You are not authorized to access this tournament details.")
        return redirect('tournaments')

    context = {
        'tournament': tournament,
        'participants': participants,
        'can_start': tournament.is_ready_to_start() and not tournament.is_started and tournament.creator == request.user,
        'user_in_tournament': user_in_tournament,
        'is_creator': tournament.creator == request.user,
    }
    return render(request, 'tournament_detail.html', context)

@login_required(login_url='/accounts/login/?redirected=true')
def tournament_start(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)

    if request.method == 'POST' and tournament.is_ready_to_start() and not tournament.is_started and tournament.creator == request.user:
        tournament.start()
        # messages.success(request, 'Tournament has started!')
        return redirect('tournament_game', tournament_id=tournament.id)
    else:
        if not tournament.is_ready_to_start():
            messages.error(request, 'The tournament is not ready to start yet.')
        elif tournament.is_started:
            messages.error(request, 'The tournament has already started.')
        else:
            messages.error(request, 'You are not authorized to start this tournament.')

    return redirect('tournament_detail', tournament_id=tournament_id)

@login_required(login_url='/accounts/login/?redirected=true')
def tournament_signup(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    if tournament.is_started:
        messages.error(request, "You cannot sign up for this tournament as it has already started.")
        return redirect('tournament_detail', tournament_id=tournament.id)

    if request.method == 'POST':
        # ctrl si l'user est deja inscrit
        if TournamentParticipant.objects.filter(tournament=tournament, player=request.user).exists():
            messages.error(request, 'You are already signed up for this tournament.')
        else:
            TournamentParticipant.objects.create(tournament=tournament, player=request.user)
            #messages.success(request, 'You have successfully signed up for the tournament.')
    return redirect('tournament_detail', tournament_id=tournament.id)

@login_required(login_url='/accounts/login/?redirected=true')
def tournament_game(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    current_match = tournament.get_current_match()
    
    if not current_match and not tournament.is_finished:
        tournament.create_next_round()
        current_match = tournament.get_current_match()
        
    current_round_matches = tournament.get_current_round_matches()

    context = {
        'tournament': tournament,
        'current_match': current_match,
        'current_round_matches': current_round_matches,
        'show_alerts': True
    }
    return render(request, 'tournament_game.html', context)

@login_required(login_url='/accounts/login/?redirected=true')    
def tournament_delete(request, tournament_id) -> HttpResponse:
    tournament = get_object_or_404(Tournament, id=tournament_id)

    # ctrl si l'user est le createur du tournoi
    if tournament.creator != request.user:
        messages.error(request, "You are not authorized to delete this tournament.")
        return redirect('tournament_detail', tournament_id=tournament.id)

    # ctrl si le tournoi a deja start
    if tournament.is_started:
        messages.error(request, "You cannot delete a tournament that has already started.")
        return redirect('tournament_detail', tournament_id=tournament.id)

    # del le tournoi
    tournament.delete()
    #messages.success(request, "Tournament has been deleted successfully.")
    return redirect('tournaments')

@login_required(login_url='/accounts/login/?redirected=true')
def submit_match_result(request, tournament_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required(login_url='/accounts/login/?redirected=true')  
def get_next_match(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    next_match = tournament.get_current_match()

    if not next_match:
        if tournament.create_next_round():
            next_match = tournament.get_current_match()
        else:
            winner = tournament.winner.username if tournament.winner else "Unknown"
            tournament.delete()
            return JsonResponse({'success': False, 'error': 'Tournament finished', 'winner': winner})

    if next_match:
        current_round_matches = [
            {
                'player1': {
                    'username': match.player1.username,
                    'alias': match.player1.profile.alias,
                },
                'player2': {
                    'username': match.player2.username,
                    'alias': match.player2.profile.alias,
                } if match.player2 else None
            }
            for match in tournament.get_current_round_matches()
        ]
        return JsonResponse({
            'success': True,
            'player1': {
                'username': next_match.player1.username,
                'alias': next_match.player1.profile.alias,
            },
            'player2': {
                'username': next_match.player2.username,
                'alias': next_match.player2.profile.alias,
            } if next_match.player2 else None,
            'current_round_matches': current_round_matches,
        })
    else:
        return JsonResponse({'success': False, 'error': 'No more matches'})
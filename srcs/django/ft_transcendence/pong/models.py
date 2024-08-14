from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from math import ceil, log2

class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    number_of_players = models.IntegerField()
    is_started = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tournaments')
    current_round = models.IntegerField(default=1)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_tournaments')
    is_finished = models.BooleanField(default=False)

    def create_next_round(self):
        current_round_matches = TournamentMatch.objects.filter(
            tournament=self,
            round_number=self.current_round
        )
        
        winners = [match.winner for match in current_round_matches if match.winner]
        
        if len(winners) > 1:
            self.current_round += 1
            for i in range(0, len(winners), 2):
                player1 = winners[i]
                player2 = winners[i+1] if i+1 < len(winners) else None
                TournamentMatch.objects.create(
                    tournament=self,
                    player1=player1,
                    player2=player2,
                    round_number=self.current_round
                )
            self.save()
            return True
        elif len(winners) == 1:
            # Le tournoi est terminé
            self.winner = winners[0]
            self.is_finished = True
            self.save()
            return False
        return False

    def get_current_match(self):
        return TournamentMatch.objects.filter(
            tournament=self,
            round_number=self.current_round,
            winner__isnull=True
        ).order_by('id').first()

    def is_ready_to_start(self):
        return self.participants.count() == self.number_of_players
    def start(self):
        self.is_started = True
        self.save()

        participants = list(self.participants.values_list('player__id', flat=True))
        n = len(participants)
        rounds = ceil(log2(n))

        for i in range(0, n, 2):
            player1_id = participants[i]
            player1 = User.objects.get(id=player1_id)
            if i + 1 < n:
                player2_id = participants[i + 1]
                player2 = User.objects.get(id=player2_id)
            else:
                player2 = None
            TournamentMatch.objects.create(
                tournament=self,
                player1=player1,
                player2=player2,
                round_number=self.current_round
            )

    def is_ready_to_start(self):
        return self.participants.count() == self.number_of_players
    def advance_to_next_match(self):
        current_match = self.get_current_match()
        if current_match:
            next_match = TournamentMatch.objects.filter(
                tournament=self,
                id__gt=current_match.id,
                winner__isnull=True
            ).order_by('id').first()
            return next_match
        return None

class TournamentParticipant(models.Model):
    tournament = models.ForeignKey(Tournament, related_name='participants', on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE)

class TournamentMatch(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player1 = models.ForeignKey(User, related_name='player1_matches', on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name='player2_matches', on_delete=models.CASCADE, null=True, blank=True)
    round_number = models.IntegerField()
    winner = models.ForeignKey(User, related_name='won_matches', on_delete=models.SET_NULL, null=True, blank=True)
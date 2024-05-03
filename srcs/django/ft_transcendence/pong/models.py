from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Tournament(models.Model):
    nb_players = models.IntegerField(choices=[(4, '4'), (8, '8'), (16, '16')])
    players = models.ManyToManyField(User)
    is_finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Tournament #{self.id}"

class TournamentMatch(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    participant1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participant1_matches')
    participant2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participant2_matches')
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='winning_matches', null=True, blank=True)
    round_number = models.PositiveIntegerField(default=1)

class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
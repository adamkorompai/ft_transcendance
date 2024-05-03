from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class UserStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_games = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    goals_scored = models.IntegerField(default=0)
    goals_conceded = models.IntegerField(default=0)
    time_played = models.IntegerField(default=0)
    nb_defense = models.IntegerField(default=0)
    match_history = ArrayField(models.JSONField(), default=list)

    def __str__(self):
        return f"{self.user.username}'s Stats"
    
class UserStatsProxy(UserStats):
    class Meta:
        proxy = True
        verbose_name = 'User Stats'
        verbose_name_plural = 'User Stats'
from django.db import models
from django.contrib.auth.models import User

class UserStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_games = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Stats"
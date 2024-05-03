import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ft_transcendence.settings')
django.setup()

from django.contrib.auth.models import User
from stats.models import UserStats

# Sup toutes les instances de UserStats
UserStats.objects.all().delete()
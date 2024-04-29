from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserStats

@login_required
def user_stats(request):
    user = request.user
    stats, created = UserStats.objects.get_or_create(user=user)
    context = {
        'stats': stats
    }
    return render(request, 'stats/user_stats.html', context)
from django.shortcuts import render

# Create your views here.
def pong_game(request):
    return render(request, 'game.html')

def play(request):
    return render(request, 'play.html')

def quick_play(request):
    return render(request, 'quickplay.html')
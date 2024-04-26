from django.shortcuts import render
from render_block import render_block_to_string
from django.http import HttpResponse

# Create your views here.
def pong_game(request):
    return render(request, 'game.html')

def play(request):
    return render(request, 'play.html')

def quick_play(request):
    if 'HTTP_HX_REQUEST' in request.META:
        context = {"request": request}
        html = render_block_to_string('quickplay.html', 'body', context)
        return HttpResponse(html)
    return render(request, 'quickplay.html')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Room, Message
from accounts.models import FriendList
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from accounts.models import Profile
from render_block import render_block_to_string
from django.middleware.csrf import get_token

# Create your views here.
@login_required
def chat_page(request):
    profile = Profile.objects.all()
    rooms = Room.objects.all()
    users = User.objects.all()
    current_user = request.user
    if current_user.is_authenticated:
        try:
            friend_list = FriendList.objects.get(user=current_user)
            friends = friend_list.friends.all()
        except FriendList.DoesNotExist:
            friends = None

    context = {
        "rooms": rooms,
        "users" : users,
        "profiles": profile,
        "friends" : friends,
        "request": request,
        'my_csrf': get_token(request),
        'title': "Chat"
    }
    if 'HTTP_HX_REQUEST' in request.META:
        html = render_block_to_string('chat.html', 'body', context)
        return HttpResponse(html)
    return render(request, "chat.html", context)

def room(request, slug):
    room_name=Room.objects.get(slug=slug).name
    messages=Message.objects.filter(room=Room.objects.get(slug=slug))

    username1, username2 = slug.split('_')
    other_username = username2 if request.user.username == username1 else username1
    other_user = get_object_or_404(User, username=other_username)
    profile = get_object_or_404(Profile, user=other_user)
    context = {"slug":slug, "room_name":room_name, 'messages':messages, 'user_id':request.user.id, 'profile':profile}
    return render(request, "room.html", context)

def create_room(request):
    if request.method == "POST":
        # Assuming 'name' and 'slug' are provided in the form submission
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        user1 = request.user
        user2_id = request.POST.get('user2_id')
        user2 = User.objects.get(id=user2_id)

        # Ensure consistent order of usernames for room slug
        user1_username = user1.username
        user2_username = user2.username
        room_slug = '_'.join(sorted([user1_username, user2_username]))

        existing_room = Room.objects.filter(slug=room_slug).exists()
        if not existing_room:
            # Create a new room
            room = Room.objects.create(name=name, slug=room_slug, user1=user1, user2=user2)
            return redirect('room', slug=room_slug)
        else:
            # Room already exists, redirect to the existing room
            return redirect('room', slug=room_slug)

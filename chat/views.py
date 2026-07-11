from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message
from .forms import CreateGroupForm

User = get_user_model()

@login_required
def inbox_view(request):
    rooms = request.user.chat_rooms.all().order_by('-created_at')
    return render(request, 'chat/inbox.html', {'rooms': rooms})

@login_required
def room_view(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id, participants=request.user)
    messages = room.messages.all()
    return render(request, 'chat/room.html', {'room': room, 'messages': messages})

@login_required
def start_direct_chat(request, username):
    other_user = get_object_or_404(User, username=username)
    if other_user == request.user:
        return redirect('chat_inbox')

    existing_room = ChatRoom.objects.filter(is_group=False, participants=request.user).filter(participants=other_user).first()
    if existing_room:
        return redirect('chat_room', room_id=existing_room.id)

    room = ChatRoom.objects.create(is_group=False)
    room.participants.add(request.user, other_user)
    return redirect('chat_room', room_id=room.id)

@login_required
def create_group_view(request):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            room = ChatRoom.objects.create(name=form.cleaned_data['name'], is_group=True)
            room.participants.add(request.user)
            for user in form.cleaned_data['participants']:
                room.participants.add(user)
            return redirect('chat_room', room_id=room.id)
    else:
        form = CreateGroupForm()
    return render(request, 'chat/create_group.html', {'form': form})
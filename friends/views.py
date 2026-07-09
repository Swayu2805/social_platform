from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import FriendRequest, Follow
from notifications.models import Notification

User = get_user_model()

@login_required
def user_list(request):
    query = request.GET.get('q', '')
    users = User.objects.exclude(id=request.user.id)
    if query:
        users = users.filter(username__icontains=query)
    return render(request, 'friends/user_list.html', {'users': users, 'query': query})

@login_required
def send_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    if to_user != request.user:
        fr, created = FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
        if created:
            Notification.objects.create(
                recipient=to_user,
                sender=request.user,
                notif_type='friend_request',
                text=f'{request.user.username} sent you a friend request.'
            )
    return redirect('user_list')

@login_required
def accept_request(request, request_id):
    fr = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    fr.status = 'accepted'
    fr.save()
    Notification.objects.create(
        recipient=fr.from_user,
        sender=request.user,
        notif_type='friend_request',
        text=f'{request.user.username} accepted your friend request.'
    )
    return redirect('request_list')

@login_required
def reject_request(request, request_id):
    fr = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    fr.status = 'rejected'
    fr.save()
    return redirect('request_list')

@login_required
def request_list(request):
    received = FriendRequest.objects.filter(to_user=request.user, status='pending')
    return render(request, 'friends/request_list.html', {'received': received})

@login_required
def follow_toggle(request, user_id):
    target = get_object_or_404(User, id=user_id)
    if target != request.user:
        follow, created = Follow.objects.get_or_create(follower=request.user, following=target)
        if not created:
            follow.delete()
        else:
            Notification.objects.create(
                recipient=target,
                sender=request.user,
                notif_type='follow',
                text=f'{request.user.username} started following you.'
            )
    return redirect('user_list')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Like, Comment
from .forms import PostForm, CommentForm
from notifications.models import Notification

@login_required
def feed_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('feed')
    else:
        form = PostForm()
    posts = Post.objects.select_related('author').prefetch_related('comments', 'likes').order_by('-created_at')
    return render(request, 'posts/feed.html', {'form': form, 'posts': posts})

@login_required
def like_toggle(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    elif post.author != request.user:
        Notification.objects.create(
            recipient=post.author,
            sender=request.user,
            notif_type='like',
            text=f'{request.user.username} liked your post.'
        )
    return redirect('feed')

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    sender=request.user,
                    notif_type='comment',
                    text=f'{request.user.username} commented on your post.'
                )
    return redirect('feed')

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('feed')
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('feed')
    return render(request, 'posts/delete_post.html', {'post': post})

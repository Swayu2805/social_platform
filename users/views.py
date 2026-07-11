from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from posts.models import Post
from friends.models import Follow
from .forms import CustomUserCreationForm, EditProfileForm
from .tokens import email_verification_token

User = get_user_model()

def send_verification_email(request, user):
    current_site = get_current_site(request)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token.make_token(user)
    link = f"http://{current_site.domain}/verify-email/{uid}/{token}/"
    message = f"Hi {user.username},\n\nPlease verify your email by clicking the link below:\n\n{link}\n\nThanks for joining Social Platform!"
    send_mail(
        'Verify your email - Social Platform',
        message,
        'noreply@socialplatform.com',
        [user.email],
        fail_silently=False,
    )

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def verification_sent_view(request):
    return render(request, 'users/verification_sent.html')

def verify_email_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'users/verify_success.html')
    else:
        return render(request, 'users/verify_failed.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            try:
                existing = User.objects.get(username=username)
                if not existing.is_active:
                    return render(request, 'users/login.html', {'error': 'Please verify your email before logging in.'})
            except User.DoesNotExist:
                pass
            return render(request, 'users/login.html', {'error': 'Invalid username or password.'})
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    return render(request, 'users/home.html')

@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user).order_by('-created_at')
    is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()
    followers_count = Follow.objects.filter(following=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()
    posts_count = posts.count()
    context = {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
        'posts_count': posts_count,
    }
    return render(request, 'users/profile.html', context)

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from posts.models import Post, Report
from django.db.models import Count

User = get_user_model()

@staff_member_required
def dashboard_home(request):
    context = {
        'total_users': User.objects.count(),
        'total_posts': Post.objects.count(),
        'total_reports': Report.objects.count(),
        'recent_reports': Report.objects.select_related('post', 'reported_by').order_by('-created_at')[:5],
    }
    return render(request, 'dashboard/home.html', context)

@staff_member_required
def reported_posts(request):
    reports = Report.objects.select_related('post', 'post__author', 'reported_by').order_by('-created_at')
    context = {'reports': reports}
    return render(request, 'dashboard/reported_posts.html', context)

@staff_member_required
def dismiss_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.delete()
    return redirect('reported_posts')

@staff_member_required
def delete_reported_post(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    post = report.post
    post.delete()
    return redirect('reported_posts')

@staff_member_required
def user_management(request):
    users = User.objects.all().order_by('-created_at')
    context = {'users': users}
    return render(request, 'dashboard/user_management.html', context)

@staff_member_required
def toggle_user_active(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if target_user != request.user:
        target_user.is_active = not target_user.is_active
        target_user.save()
    return redirect('user_management')

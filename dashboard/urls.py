from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('reports/', views.reported_posts, name='reported_posts'),
    path('reports/dismiss/<int:report_id>/', views.dismiss_report, name='dismiss_report'),
    path('reports/delete-post/<int:report_id>/', views.delete_reported_post, name='delete_reported_post'),
    path('users/', views.user_management, name='user_management'),
    path('users/toggle/<int:user_id>/', views.toggle_user_active, name='toggle_user_active'),
]

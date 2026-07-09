from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('request/send/<int:user_id>/', views.send_request, name='send_request'),
    path('request/accept/<int:request_id>/', views.accept_request, name='accept_request'),
    path('request/reject/<int:request_id>/', views.reject_request, name='reject_request'),
    path('requests/', views.request_list, name='request_list'),
    path('follow/<int:user_id>/', views.follow_toggle, name='follow_toggle'),
]

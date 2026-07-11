from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.inbox_view, name='chat_inbox'),
    path('chat/room/<int:room_id>/', views.room_view, name='chat_room'),
    path('chat/start/<str:username>/', views.start_direct_chat, name='start_direct_chat'),
    path('chat/group/create/', views.create_group_view, name='create_group'),
]
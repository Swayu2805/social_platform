from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, PostViewSet, CommentViewSet, LikeViewSet,
    FriendRequestViewSet, FollowViewSet, NotificationViewSet
)

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('posts', PostViewSet)
router.register('comments', CommentViewSet)
router.register('likes', LikeViewSet)
router.register('friend-requests', FriendRequestViewSet)
router.register('follows', FollowViewSet)
router.register('notifications', NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

@receiver(post_save, sender=Notification)
def send_notification_ws(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        group_name = f"user_{instance.recipient.id}_notifications"
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_notification",
                "data": {
                    "text": instance.text,
                    "notif_type": instance.notif_type,
                    "created_at": instance.created_at.strftime('%b %d, %Y, %I:%M %p'),
                }
            }
        )


from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from .models import Message, ChatRoom

# Custom signal
message_sent = Signal()

@receiver(post_save, sender=Message)
def notify_new_message(sender, instance, created, **kwargs):
    if created:
        # Broadcast to all users in the chat room
        message_sent.send(sender=sender, message=instance)
        print("New message in room ")

# @receiver(message_sent)
# def handle_new_message(sender, message, **kwargs):
#     # You can perform additional actions here, like sending notifications
#     print(f"New message in room {message.room.name}: {message.content}")


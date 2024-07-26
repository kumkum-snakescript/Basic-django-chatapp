from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    user1 = models.ForeignKey(User, related_name='chatroom_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='chatroom_user2', on_delete=models.CASCADE)
    room_name = models.CharField(max_length=64, unique=True, default='room1')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatRoom between {self.user1.username} and {self.user2.username}"

    @staticmethod
    def get_or_create_chat_room(user1, user2):
        users = sorted([user1, user2], key=lambda u: u.username)
        room_name = f"chat_{users[0].username}_{users[1].username}"
        chat_room, created = ChatRoom.objects.get_or_create(
            user1=users[0], user2=users[1],
            defaults={'room_name': room_name}
        )
        return chat_room

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"
    

    # class Relation(models.Model):
    # user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="relation_user1")
    # user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="relation_user2")
    # message = models.TextField()

    # class Meta:
    #     app_label='auth'

    # class Chat(models.Model):
    # username = models.ForeignKey(User, on_delete=models.CASCADE)
    # message = models.TextField(null=False)
    # timestamp = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     app_label='auth'
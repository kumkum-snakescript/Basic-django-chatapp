from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'auth'


class Relation(models.Model):
    user1 = models.ForeignKey(User,on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(User,on_delete=models.CASCADE, related_name="user2")
    message = models.TextField()

    class Meta:
        app_label = 'auth'


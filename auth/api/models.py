from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db import models
from shortuuidfield import ShortUUIDField

class User(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True)
    otp_code = models.CharField(max_length=6, null=True)
    is_verified = models.BooleanField(default=False)
    birth_date = models.DateField(blank=True, null=True)
    zipcode = models.IntegerField(blank=True, null=True)


class ChatRoom(models.Model):
	roomId = ShortUUIDField()
	type = models.CharField(max_length=10, default='DM')
	member = models.ManyToManyField(User)
	name = models.CharField(max_length=20, null=True, blank=True)
	room_created_by = models.ForeignKey(User,related_name="room_createdBy",on_delete=models.CASCADE,null=True)
	context = models.CharField(max_length=200,choices=[['allow','Allow'],['deny',"Deny"],['no','No']],null=True,default="no")

	def __str__(self):
		return self.roomId + ' -> ' + str(self.name)
	
class ChatMessage(models.Model):
	MESSAGE_TYPES = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
		('file', 'File')
        # Add more message types as needed
    )

	chat = models.ForeignKey(ChatRoom, on_delete=models.SET_NULL, null=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	message = models.CharField(max_length=255)
	timestamp = models.DateTimeField(auto_now_add=True)
	is_read  = models.BooleanField(default=False)
	message_type = models.CharField(max_length=10,blank=True,null=True)

	def __str__(self):
		return self.message
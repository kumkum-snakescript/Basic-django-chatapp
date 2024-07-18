import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import os
from asgiref.sync import sync_to_async
from api.models import *
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

def getUser(userId):
    return User.objects.get(id=userId)

@database_sync_to_async
def mark_message_read(userId, roomId):
    chatroom = ChatRoom.objects.get(roomId=roomId)
    users = chatroom.member.all().exclude(id=userId)
    ChatMessage.objects.filter(chat=chatroom, user_id=users[0], is_read=False).update(is_read=True)

    return 'ok'


connected_users = set()
class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.online_users = {}

    async def connect(self):
        self.roomId = self.scope["url_route"]["kwargs"]["userId"]
        self.byte_string = self.scope["query_string"]
        self.string_data = self.byte_string.decode("utf-8")
        self.access_token = self.string_data.split("=")[1]
        # get user from access token
        self.token_data = AccessToken(self.access_token)

        self.user = await getUser(self.token_data.payload["user_id"])
        self.userId = self.user.id
        self.first_name = self.user.first_name
        self.last_name = self.user.last_name

        self.room_group_name = "chat_%s" % self.roomId
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        connected_users.add(self.user)
        print(len(connected_users),"-----HERE------")

        self.userlen = len(connected_users)

        await self.set_user_online_status(True,self.user,self.roomId)
        
        await self.accept()


        await mark_message_read(self.userId, self.roomId)

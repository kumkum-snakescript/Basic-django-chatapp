import django
django.setup()
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'basic_app.settings')

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Message
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.other_username = self.scope['url_route']['kwargs']['username']
        self.other_user = await database_sync_to_async(User.objects.get)(username=self.other_username)
        self.chat_room = await database_sync_to_async(ChatRoom.get_or_create_chat_room)(self.user, self.other_user)
        self.room_group_name = f"chat_{self.chat_room.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Save the message to the database
        await database_sync_to_async(Message.objects.create)(
            chat_room=self.chat_room,
            sender=self.user,
            content=message
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
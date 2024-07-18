from django.urls import path
from auth.api import consumer

websocket_urlpatterns = [
    path('ws/chat-cosnumer/', consumer.ChatConsumer.as_asgi()),
    
]


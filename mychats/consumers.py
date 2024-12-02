# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import UserMessage
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['username']
        self.room_group_name = f'chat_{self.room_name}'

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
        data = json.loads(text_data)
        message = data.get('message', '')
        image = data.get('image', None)
        file = data.get('file', None)
        sender_username = data.get('sender')

        # Get sender and recipient users
        sender = User.objects.get(username=sender_username)
        recipient_username = data.get('recipient')
        recipient = User.objects.get(username=recipient_username)

        # Save message to the database
        user_message = UserMessage.objects.create(
            sender=sender,
            recipient=recipient,
            text=message,
            image=image,
            files=file
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'image': image,
                'file': file,
                'sender': sender.username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        image = event['image']
        file = event['file']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'image': image,
            'file': file,
            'sender': sender,
        }))
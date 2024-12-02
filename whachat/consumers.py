# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']
        self.room_group_name = f'chat_{self.username}'
        
        # Add this user to the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        # Remove this user from the group when they disconnect
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', None)
        is_typing = text_data_json.get('is_typing', False)
        user = self.scope['user']

        if is_typing:
            # Broadcast "user is typing" to all group members
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_typing',
                    'user': user.username
                }
            )
        elif message:
            # Save the message to the database asynchronously
            await self.save_message(user, message)

            # Broadcast the message to all group members
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': user.username
                }
            )

    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user
        }))

    async def user_typing(self, event):
        user = event['user']

        # Send the typing notification to WebSocket
        await self.send(text_data=json.dumps({
            'typing': True,
            'user': user
        }))

    
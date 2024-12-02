import json
import logging
import base64
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Message
from channels.db import database_sync_to_async
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)
User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.user = self.scope['user']
            self.other_username = self.scope['url_route']['kwargs']['username']

            # Ensure group name is consistent by sorting the usernames
            usernames = sorted([self.user.username, self.other_username])
            self.room_group_name = f"chat_{usernames[0]}_{usernames[1]}"

            # Join the group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        except Exception as e:
            logger.error(f"Connection error: {e}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            # Leave the group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        except Exception as e:
            logger.error(f"Disconnection error: {e}")

    async def receive(self, text_data=None, bytes_data=None):
        try:
            if text_data:
                # Handle text messages
                text_data_json = json.loads(text_data)
                message = text_data_json.get('message', '')

                # Save the text message to the database
                await self.save_message(message=message)

                # Broadcast the text message to the group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'user': self.user.username,
                        'image': None,
                    }
                )

            elif bytes_data:
                # Handle image messages (binary data)
                # Validate image size (optional, prevent very large images)
                if len(bytes_data) > 10 * 1024 * 1024:  # 10MB limit
                    logger.warning("Image too large")
                    return

                # Determine file extension (you might want to improve this)
                import imghdr
                image_type = imghdr.what(None, h=bytes_data)
                if not image_type:
                    logger.warning("Invalid image type")
                    return

                # Generate a unique filename
                image_name = f"chat_image_{timezone.now().timestamp()}.{image_type}"
                image = ContentFile(bytes_data, name=image_name)

                # Save the image to the database
                saved_message = await self.save_message(image=image)

                # Encode the image as Base64 for transmission
                encoded_image = base64.b64encode(bytes_data).decode('utf-8')

                # Broadcast the image message to the group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': None,
                        'user': self.user.username,
                        'image': encoded_image,
                        'image_type': image_type,
                    }
                )

        except json.JSONDecodeError:
            logger.error("Invalid JSON data")
        except Exception as e:
            logger.error(f"Message receiving error: {e}")

    async def chat_message(self, event):
        # Send the message (text or image) to WebSocket
        try:
            await self.send(text_data=json.dumps({
                'message': event.get('message'),
                'user': event.get('user'),
                'image': event.get('image'),
                'image_type': event.get('image_type')
            }))
        except Exception as e:
            logger.error(f"Message sending error: {e}")

    @database_sync_to_async
    def save_message(self, message=None, image=None):
        """
        Save text or image message to the database.
        """
        try:
            return Message.objects.create(
                user=self.user,
                receiver=User.objects.get(username=self.other_username),
                message=message,
                image=image
            )
        except Exception as e:
            logger.error(f"Message saving error: {e}")
            raise
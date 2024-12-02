from django.db import models
from django.contrib.auth import get_user_model



User = get_user_model()


class UserMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reci')
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='chats_messages', blank=True)
    files = models.FileField(upload_to='chat_files')
    active = models.BooleanField(default=True)
    edited = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.text[:10]

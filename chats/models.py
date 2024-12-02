from django.db import models
import uuid
from django.contrib.auth import get_user_model


User = get_user_model()




class Messages(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, blank=False, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipients')
    text = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    files = models.FileField(upload_to='chat_files', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.text[:10]


    

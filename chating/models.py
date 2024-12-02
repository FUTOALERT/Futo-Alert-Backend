from django.db import models
from django.conf import settings
import cv2

class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # User who sent the message
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_messages")  # User who received the message
    message = models.TextField(blank=True, null=True)  # Message content (optional)
    image = models.ImageField(upload_to='chat_images/', blank=True, null=True)  # New field for image uploads
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp when the message was sent
    is_read = models.BooleanField(default=False)  # Flag to check if the message was read 

    def __str__(self):
        return f"Message from {self.user} to {self.receiver} at {self.timestamp}"

    class Meta:
        ordering = ['timestamp']  
        
        
        
        
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            image = cv2.imread(self.image.path)
            height, width = (500, 300)
            size = (height, width)
            image = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
            cv2.imwrite(self.image.path, image)    
        
        
        
    def get_user_chat_message_image(self):
        if self.image:
            return self.image.url
        else:
            pass
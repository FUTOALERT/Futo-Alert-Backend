from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
import uuid
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
import cv2
from django.conf import settings

class UserManager(BaseUserManager):
    """ 
    A blueprint to create a user class
    """
    
    def create_user(self, username, email, phone_number, password,  **kwargs):
        """
        A method to create a user manager
        """
        if not username:
            raise ValidationError("UserName Field Must Be Filled")
        if not email:
            raise ValidationError("Email Field Must Be Filled")
        if not phone_number:
            raise ValidationError("Phone Number Must Be Filled")
        if not password:
            raise ValidationError("Password Field Must Be Filled")
        
        user = self.model(username=username, email=self.normalize_email(email), phone_number=phone_number, password=password, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_superuser(self, username, email, phone_number, password, **kwargs):
        """
        A method to create a superuser
        """
        if not username:
            raise ValidationError("UserName Field Is Required")
        if not email:
            raise ValidationError("Email Field Is Required")
        if not phone_number:
            raise ValidationError("Phone Number Field Must Be Required")
        if not password:
            raise ValidationError("Password Field Must Be Required")
        
        user = self.model(username=username, email=self.normalize_email(email), phone_number=phone_number, password=password, **kwargs)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
            


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(unique=True, primary_key=True, editable=False, default=uuid.uuid4)
    username = models.CharField(max_length=256, unique=True)
    first_name = models.CharField(max_length=256, db_index=True)
    last_name = models.CharField(max_length=256, db_index=True)
    email = models.EmailField(unique=True, max_length=100, db_index=True)
    phone_number = PhoneNumberField(unique=True)
    image = models.ImageField(upload_to='users_images', blank=True)
    cover_image = models.ImageField(upload_to='cover_image', blank=True)
    country = models.CharField(max_length=256, blank=True)
    address = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.name
    
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            image = cv2.imread(self.image.path)
            height, width = (100, 100)
            size = (height, width)
            image = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
            cv2.imwrite(self.image.path, image)
            
            
        if self.cover_image:
            cover_photo = cv2.imread(self.cover_image.path)
            heights, widths = (960, 250)
            sizes = (heights, widths)    
            cover_photos = cv2.resize(cover_photo, sizes, interpolation=cv2.INTER_AREA)
            cv2.imwrite(self.cover_image.path, cover_photos)
        else:
            pass  
    
    
    
    
    @property
    def name(self):
        return f"{self.first_name} {self.username}"
    
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['phone_number', 'username']
    
    
    
    
    def get_user_image(self):
        if self.image:
            return self.image.url
        else:
            return settings.MEDIA_URL + "usersimage.jpg"
        
        
    def get_user_cover_image(self):
        if self.cover_image:
            return self.cover_image.url
        else:
            return settings.MEDIA_URL + "usercovers.png"     
    

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


User = get_user_model()


class EmailOrPhoneNumberBackend(ModelBackend):
    def authenticate(self, request, identifier, password, **kwargs):
        """
        A method to authenticate by email or phone number
        """
        try:
            user = User.objects.get(email=identifier)
            return user
        except User.DoesNotExist:
            try:
                user = User.objects.get(phone_number=identifier)
            except User.DoesNotExist:
                return None
        
        if user.check_password(password):
            return user
        return None
            
                
from django import forms

from users.models import User


class User_Update_Form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'country', 'address', 'city', 'image', 'cover_image', 'postal_code', 'bio']
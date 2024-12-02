from django.shortcuts import render
from .models import Messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


User = get_user_model()


@login_required
def user_chats(request, username):
    user = request.user
    messages = Messages
    return render(request, 'users/default-message.html', {'user': user})
from django.shortcuts import render, get_object_or_404
from django.db.models import Q  # Import Q for complex queries
from users.models import User
from .models import Message

def user_one_chat(request, username):
    other_user = get_object_or_404(User, username=username)  # Chatting partner
    current_user = request.user  # Logged-in user

    # Get the chat history between the current user and the other user
    messages = Message.objects.filter(
        (Q(user=current_user) & Q(receiver=other_user)) | 
        (Q(user=other_user) & Q(receiver=current_user))
    ).order_by('timestamp')  # Order messages by timestamp
    
    return render(request, 'users/my-chat.html', {
        'other_user': other_user,
        'current_user': current_user,
        'messages': messages,  # Pass messages to the template
    })

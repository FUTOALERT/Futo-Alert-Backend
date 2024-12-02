from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.models import User
from django.db.models import Q  # Import Q to filter messages
from .models import UserMessage

@login_required
def chat_views_user(request, username):
    # Get the recipient user object
    recipient = get_object_or_404(User, username=username)
    users = User.objects.exclude(username=request.user.username)
    
    # Get the logged-in user
    sender = request.user

    # Fetch all messages between the sender and recipient
    messages = UserMessage.objects.filter(
        (Q(sender=sender) & Q(recipient=recipient)) |
        (Q(sender=recipient) & Q(recipient=sender))
    ).order_by('created')

    # Render the chat template with both users and the messages
    return render(request, 'users/default-message.html', {
        'recipient': recipient,
        'user': sender,
        'messages': messages,
        'users': users,
    })

    
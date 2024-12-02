from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


User = get_user_model()



@login_required
def users_chattings(request, username):
        # Get the recipient user object
    recipient = get_object_or_404(User, username=username)
    users = User.objects.exclude(username=request.user.username)
    
    # Get the logged-in user
    sender = request.user

    # Fetch all messages between the sender and recipient
    

    # Render the chat template with both users and the messages
    return render(request, 'users/chatting.html', {
        'recipient': recipient,
        'user': sender,
        'users': users,
    })

    
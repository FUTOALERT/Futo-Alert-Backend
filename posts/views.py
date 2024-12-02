from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


User = get_user_model()




def get_logged_in_user(request):
    user = request.user
    return {'user': user}


def front_page(request):
    if request.user.is_authenticated:
        users = User.objects.exclude(username=request.user.username)
        return render(request, 'users/default.html', {'users': users})
    else:
        return redirect('user_login')
    

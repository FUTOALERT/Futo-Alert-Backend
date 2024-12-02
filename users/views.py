import django.contrib.auth.decorators
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import User_Update_Form
from django.shortcuts import get_object_or_404


User = get_user_model()



def user_login(request):
    """
    A method to login in a user
    """
    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        print("This is the users identifier", identifier)
        password = request.POST.get('password')
        
        user = authenticate(request, identifier=identifier, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'LOGGED IN SUCCESFULLY')
                return redirect('home')
            else:
                messages.error(request, 'CORRECT THE ERROR BELOW')
                return redirect('user_login')
        else:
            messages.error(request, 'ACCOUNT DOES NOT EXIST')
            return redirect('user_login')
            
    else:
        return render(request, 'users/login.html')      
    
    
    

def user_registers(request):
    """
    A method to register a user
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'USERNAME ALREADY EXISTS')
            return redirect('user_register')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'EMAIL ALREADY EXISTS')
            return redirect('user_register')
        elif User.objects.filter(phone_number=phone_number).exists():
            messages.error(request, 'USER WITH PHONE NUMBER EXISTS')
            return redirect('user_register')
        elif password != confirm_password:
            messages.error(request, 'PASSWORD ARE NOT MATCHING')
            return redirect('user_register')
        User.objects.create_user(username=username, email=email, phone_number=phone_number, password=password)
        return redirect('user_login')
    return render(request, 'users/register.html')
                  
            
            
            
            
@login_required
def user_update_account(request, username):
    if request.user.username != username:
        messages.error(request, 'YOU CANNOT UPDATE A PROFILE THAT IS NOT YOURS')
        return redirect('home')
    else:
        pass 
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = User_Update_Form(instance=user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'PROFILE UPDATED SUCCESSFULLY')
        else:
            messages.error(request, 'CORRECT THE ERROR BELOW')
    else:
        form = User_Update_Form(instance=user)        
    return render(request, 'users/account-information.html', {'form': form, 'user': user})
    
    
    
@login_required    
def author_profile_detail(request, username):
    author_user = get_object_or_404(User, username=username)
    return render(request, 'users/user-page.html', {'author_user': author_user})    
    
    
@login_required    
def get_user_settings(request, username):
    if request.user.username != username:
        return redirect('home')
    else:
        return render(request, 'users/default-settings.html', )    
                    
                    
    
        
    
                


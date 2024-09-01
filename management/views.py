from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


def index(request):
    return render(request, 'management/index.html')
    
def home(request):
    return render(request, 'management/home.html')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'management/login.html')

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
    
#         if user is not None:
#             login(request, user)
#             return redirect('protected_view')
#         else:
#             # Add an error message to be displayed in the template
#             messages.error(request, 'Invalid username or password.')
#             return render(request, 'management/login.html', {'error': 'Invalid credentials'})
#     return redirect('management/login_page')

def auth_logout(request):
    if request.user.is_authenticated:
        # Logout the user
        logout(request)
        # Invalidate the user's session
        request.session.flush()
        # Generate a new session key
        request.session.create() 
        # Update the user's session hash to prevent reuse of old sessions
        update_session_auth_hash(request, request.user)
        messages.success(request, "You have been successfully logged out and un-authenticated.")
    else:
        messages.info(request, "You were not logged in.")
    
    return redirect('index')

def logout_view(request):
    auth_logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('index')
    
@login_required
def protected_view(request):
    return render(request,'management/protected.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'management/change_password.html', {
        'form': form
    })
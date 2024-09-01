from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .models import Assistant
from .forms import AssistantForm
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
def account_details(request):
    return render(request,'management/account_details.html')

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
    

@login_required
def assistant_edit(request, slug=None):
    # Fetch all assistants for the selection dropdown
    assistants = Assistant.objects.all()
    # Check if an assistant is selected for editing using the slug
    if slug:
        assistant = get_object_or_404(Assistant, slug=slug)
    else:
        raise ValueError('slug is not valid')
    # Process the form submission
    if request.method == 'POST':
        form = AssistantForm(request.POST, instance=assistant)
        if form.is_valid():
            form.save()
            # Redirect back to the same page after saving to allow further editing
            return redirect('assistant_edit', slug=form.instance.slug)
    else:
        form = AssistantForm(instance=assistant)

    # Render the template with the selection and edit form
    return render(request, 'management/assistant_edit.html', {'form': form, 'assistants': assistants, 'selected_assistant': assistant})

@login_required
def assistant_list(request):
    assistants = Assistant.objects.all()  # Retrieve all Assistant objects
    return render(request, 'management/assistant_list.html', {'assistants': assistants})
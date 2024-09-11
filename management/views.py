from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import project.settings  as project_settings
import logging

logger = logging.getLogger(__name__)
import json

from .models import AssistantModel
from .forms import AssistantForm

from vapi_api.assistant import VAPIAssistant
vapi = VAPIAssistant() # VapiClient is init

def index(request):
    return render(request, 'management/index.html')
    
def home(request):
    return render(request, 'management/home.html')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    return render(request, 'management/login.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
    
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Add an error message to be displayed in the template
            messages.error(request, 'Invalid username or password.')
            return render(request, 'management/login.html', {'error': 'Invalid credentials'})
    return redirect('management/home.html')

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
    assistants = AssistantModel.objects.all()
    
    # Check if an assistant is selected for editing using the slug
    if slug:
        assistant = get_object_or_404(AssistantModel, slug=slug)
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
    assistants = AssistantModel.objects.all()  # Retrieve all Assistant objects
    return render(request, 'management/assistant_list.html', {'assistants': assistants})



@login_required
@csrf_exempt
@require_http_methods(["POST"])
def create_assistant(request):
    data = json.loads(request.body) 
    ### Filter out data {url : "/gdgfd" , name : "32132" , messages: [{role:"system", message : "user prompt input "}] }
    try:
        assistant = vapi.create_assistant(**data)
        assistant.save_to_db()
        return JsonResponse({"result" : True, "success" : True}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
@login_required
@require_http_methods(["GET"])
def list_assistants(request):
    try:
        assistants = vapi.list_assistants()
        return JsonResponse([assistant.__dict__ for assistant in assistants], safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
@login_required
@require_http_methods(["GET"])
def get_assistant(request, assistant_id):
    try:
        assistant = vapi.get_assistant(assistant_id)
        return JsonResponse(assistant.__dict__)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=404)
@login_required
@csrf_exempt
@require_http_methods(["PATCH"])
def update_assistant(request, assistant_id):
    data = json.loads(request.body)
    try:
        updated_assistant = vapi.update_assistant(assistant_id, **data)
        return JsonResponse(updated_assistant.__dict__)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_assistant(request, assistant_id):
    try:
        vapi.delete_assistant(assistant_id)
        return JsonResponse({"message": "Assistant deleted successfully"}, status=204)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=404)
    
from openai_api.openai_client import InformationExtractor
from typing import List, Dict, Any

## CALL HANDLER
class CallHandler:
    def __init__(self, json_data: str):
        self.data = json.loads(json_data)
        self.call_id = self._extract_call_id()
        self.user_content = self._extract_user_content()

    def _extract_call_id(self) -> str:
        return self.data['message']['toolCalls'][0]['id']

    def _extract_user_content(self) -> str:
        messages = self.data['message']['artifact']['messagesOpenAIFormatted']
        return next((m['content'] for m in messages if m['role'] == 'user'), "")

    def get_call_id(self) -> str:
        return self.call_id

    def get_user_content(self) -> str:
        return self.user_content



@csrf_exempt
def root_view(request):
    
    ## initliza session manager
    #session_manager = SessionManager()
    if request.method == 'POST':
        # Handle POST request
        data = json.loads(request.body, strict=False)
        file_name = "output.json"
        # Write the data to a JSON file
        with open(file_name, "w") as json_file:
            json.dump(data, json_file, indent=4)
        # Accessing different parts of the dat
        if data['message']['type'] == 'tool-calls':
            data = json.loads(request.body)
            handler = CallHandler(json.dumps(data))
            call_id = handler.get_call_id()
            user_content = handler.get_user_content()

            extractor = InformationExtractor(
                system_prompt="You are an AI assistant that extracts and interprets date and time information from user input. Please convert relative time expressions to absolute dates and times based on the current date and time provided.",
                assistant_prompt={
                    "task": "Extract booking date and time",
                    "format": {
                        "booking_datetime": "YYYY-MM-DD HH:MM:SS"
                    }
                },
                model="gpt-3.5-turbo"
            )

            extracted_info = extractor.extract(user_content)

            
            _ = send_to_ngrok(data_to_send)
            #print(_)
        #if(data[0] == 'conversation-update'):
        #    print(data['content'])
        return JsonResponse({"message": "Received POST request at root"})
    return JsonResponse({"message": "Hello from Django root!"})
import requests

def send_to_ngrok(data):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {project_settings.VAPI_API_TOKEN}"
    }
    try:
        response = requests.post(project_settings.NGROK_URL, json=data, headers=headers)
        print(response.status_code)

        response.raise_for_status()
        return response.json()
    except requests.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        logger.error(f"Response content: {http_err.response.text}")
        raise
    except requests.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise
##CAL HANDLER
@csrf_exempt
@require_http_methods(["GET"])
def call_listen(request):
    response = requests.get(project_settings.NGROK_URL)
    return JsonResponse({"body": response.body})

### PROXY HANDLER TODO sil bunu?
from django.views import View
class ProxyView(View):
    def dispatch(self, request, *args, **kwargs):
        # Determine the target URL
        path = request.get_full_path()
        if request.headers.get('X-Should-Route-To'):
            url = request.headers['X-Should-Route-To'] + path
        else:
            url = f'http://localhost:8081{path}'

        # Forward the request
        method = request.method.lower()
        request_kwargs = {
            'method': method,
            'url': url,
            'headers': {key: value for (key, value) in request.headers.items() if key.lower() != 'host'},
            'data': request.body,
            'cookies': request.COOKIES,
            'allow_redirects': False,
        }

        if method == 'get':
            request_kwargs['params'] = request.GET

        response = requests.request(**request_kwargs)

        # Prepare and send the response
        django_response = HttpResponse(
            content=response.content,
            status=response.status_code,
        )

        excluded_headers = ['content-encoding', 'transfer-encoding', 'connection']
        for header, value in response.headers.items():
            if header.lower() not in excluded_headers:
                django_response[header] = value

        return django_response
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
from datetime import datetime
from restaurants.models import Restaurant
from .restaurant_manager import restaurant_manager

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

class CallSession:
    def __init__(self, call_id: str):
        self.call_id = call_id
        self.data: Dict[str, Any] = {}
        self.handler: CallHandler = None
        self.processed_data: Dict[str, Any] = {}
        self.internal_results: List[Dict[str, Any]] = []

    def update_data(self, new_data: Dict[str, Any]):
        self.data.update(new_data)

    def set_handler(self, json_data: str):
        self.handler = CallHandler(json_data)

    def process_data(self):
        if self.handler:
            user_content = self.handler.get_user_content()
            
            extractor = InformationExtractor(
                system_prompt="""You are an AI assistant that extracts and interprets date and time information from user input.
                Please convert relative time expressions to absolute dates and times based on the current date and time provided.""",
                assistant_prompt={
                    "task": "Extract booking date and time",
                    "format": {
                        "booking_datetime": "YYYY-MM-DD HH:MM:SS"
                    }
                },
                model="gpt-3.5-turbo"
            )

            extracted_info = extractor.extract(user_content)
            
            self.processed_data = {
                "call_id": self.call_id,
                "extracted_info": extracted_info
            }

    def validate_booking_datetime(self, booking_datetime: str) -> Dict[str, Any]:
        restaurant_id = self.data.get('restaurant_id')
        if not restaurant_id:
            return {"is_valid": False, "reason": "Restaurant ID not provided"}
        
        return restaurant_manager.validate_booking_datetime(restaurant_id, booking_datetime)

    def check_restaurant_availability(self, booking_datetime: str) -> Dict[str, Any]:
        restaurant_id = self.data.get('restaurant_id')
        if not restaurant_id:
            return {"is_available": False, "reason": "Restaurant ID not provided"}
        
        party_size = self.data.get('party_size', 2)  # Default to 2 if not specified
        duration = self.data.get('duration', 120)  # Default to 120 minutes if not specified
        
        availability = restaurant_manager.check_restaurant_availability(restaurant_id, booking_datetime, party_size, duration)
        
        if not availability['is_available']:
            alternative_times = restaurant_manager.suggest_alternative_times(restaurant_id, booking_datetime, party_size, duration)
            availability['alternative_times'] = alternative_times

        return availability

    def perform_internal_processes(self):
        # Process 1: Validate booking date and time
        booking_datetime = self.processed_data.get('extracted_info', {}).get('booking_datetime')
        if booking_datetime:
            validation_result = self.validate_booking_datetime(booking_datetime)
            self.internal_results.append({
                "process": "booking_validation",
                "result": validation_result
            })

            # Process 2: Check restaurant availability
            if validation_result.get('is_valid', False):
                availability_result = self.check_restaurant_availability(booking_datetime)
                self.internal_results.append({
                    "process": "availability_check",
                    "result": availability_result
                })

    def prepare_ngrok_data(self):
        result_string = f"Extracted booking information: {json.dumps(self.processed_data['extracted_info'])}\n"
        result_string += f"Internal processing results: {json.dumps(self.internal_results)}"

        # If alternative times were suggested, add them to the result string
        availability_check = next((result for result in self.internal_results if result['process'] == 'availability_check'), None)
        if availability_check and 'alternative_times' in availability_check['result']:
            alternative_times = availability_check['result']['alternative_times']
            if alternative_times['success']:
                result_string += f"\nAlternative booking times: {', '.join(alternative_times['alternative_times'])}"
            else:
                result_string += f"\nNo alternative times available: {alternative_times['reason']}"

        return {
            "results": [
                {
                    "toolCallId": self.call_id,
                    "result": result_string
                }
            ]
        }

    def send_to_ngrok(self): # Send data to GATEWAY!
        ngrok_data = self.prepare_ngrok_data()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {project_settings.VAPI_API_TOKEN}"
        }
        try:
            response = requests.post(project_settings.NGROK_URL, json=ngrok_data, headers=headers)
            response.raise_for_status()
            logger.info(f"Data sent to ngrok successfully for call_id: {self.call_id}")
            return response.json()
        except requests.HTTPError as http_err:
            logger.error(f"HTTP error occurred while sending data to ngrok for call_id {self.call_id}: {http_err}")
            logger.error(f"Response content: {http_err.response.text}")
            raise
        except requests.RequestException as req_err:
            logger.error(f"Request exception occurred while sending data to ngrok for call_id {self.call_id}: {req_err}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred while sending data to ngrok for call_id {self.call_id}: {e}")
            raise

import threading
from collections import defaultdict

class SessionManager:
    def __init__(self):
        self.sessions = defaultdict(lambda: {'lock': threading.Lock(), 'session': None})
        self.global_lock = threading.Lock()

    def get_or_create_session(self, call_id: str) -> CallSession:
        with self.global_lock:
            session_data = self.sessions[call_id]
        
        with session_data['lock']:
            if session_data['session'] is None:
                session_data['session'] = CallSession(call_id)
            return session_data['session']

    def update_session(self, call_id: str, json_data: str):
        session_data = self.sessions[call_id]
        with session_data['lock']:
            session = session_data['session']
            if session is None:
                session = CallSession(call_id)
                session_data['session'] = session
            
            session.set_handler(json_data)
            session.process_data()
            session.perform_internal_processes()
            return session.send_to_ngrok()

    def get_session_data(self, call_id: str) -> Dict[str, Any]:
        session_data = self.sessions[call_id]
        with session_data['lock']:
            return session_data['session'].data if session_data['session'] else {}

# Initialize the SessionManager
session_manager = SessionManager()

@csrf_exempt
def process_gateway_request(request):
    if request.method == 'POST':
        json_data = request.body.decode('utf-8')
        data = json.loads(json_data)
        
        # Extract the call_id from the incoming data
        call_id = data['message']['toolCalls'][0]['id']
        
        # Create or get the session
        session = session_manager.get_or_create_session(call_id)
        
        # Set the restaurant_id in the session data
        # You'll need to determine how to get the restaurant_id from the incoming data
        # This is just an example, adjust according to your actual data structure
        restaurant_id = data.get('restaurant_id') # TODO: This restaurant_id is not in the data! And it shoul be handled in when client signed in and create the assistant!
        if restaurant_id:
            session.data['restaurant_id'] = restaurant_id
        
        try:
            # Update the session with the new data, process it, and send to ngrok
            ngrok_response = session_manager.update_session(call_id, json_data)
            
            return JsonResponse({
                "message": "Received POST request at root, processed data, and sent to ngrok",
                "call_id": call_id,
                "ngrok_response": ngrok_response
            })
        except Exception as e:
            logger.error(f"Error processing request for call_id {call_id}: {str(e)}")
            return JsonResponse({
                "error": "An error occurred while processing the request",
                "call_id": call_id
            }, status=500)
    
    return JsonResponse({"message": "Hello from Django root!"})




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
import json
import uuid
import requests
from django.http import JsonResponse
import project.settings as project_settings
import logging

logger = logging.getLogger(__name__)

class Session:
    def __init__(self, session_id):
        self.session_id = session_id # This will be callID
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)

class SessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self):
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = Session(session_id)
        return session_id

    def get_session(self, session_id):
        return self.sessions.get(session_id)

    def delete_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]

class MessageProcessor:
    def __init__(self):
        # Initialize OpenAI API client here
        pass

    def process_message(self, message):
        # Process message using OpenAI API
        # This is a placeholder for the actual implementation
        ## TODO: send message to OpenAI to get exact date of reservation.
        return f"Processed: {message}"

class NGROKConnector:
    def __init__(self):
        self.url = project_settings.NGROK_URL
        self.token = project_settings.VAPI_API_TOKEN

    def send_message(self, data):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        try:
            response = requests.post(self.url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error sending message to NGROK: {e}")
            raise

session_manager = SessionManager()
message_processor = MessageProcessor()
ngrok_connector = NGROKConnector()
from api.client import APIClient
from api.config import DEFAULT_TRANSCRIBER_CONFIG, DEFAULT_MODEL_CONFIG, DEFAULT_VOICE_CONFIG
import datetime
import json
       
from management.models import AssistantModel
from datetime import datetime

class Call:
    def __init__(self, data):
        # Unique identifier for the call
        self.id = data.get('id')
        # Organization ID associated with the call
        self.org_id = data.get('orgId')
        # Name of the call
        self.name = data.get('name')
        # Type of the call (e.g., 'inboundPhoneCall')
        self.type = data.get('type')
        # ID of the assistant handling the call
        self.assistant_id = data.get('assistantId')
        # ID of the squad associated with the call (if applicable)
        self.squad_id = data.get('squadId')
        # ID of the phone number used for the call
        self.phone_number_id = data.get('phoneNumberId')
        # ID of the customer associated with the call
        self.customer_id = data.get('customerId')
        # Current status of the call (e.g., 'queued', 'in-progress', 'completed')
        self.status = data.get('status')
        # Reason for call ending (if applicable)
        self.ended_reason = data.get('endedReason')
        # Provider of the phone call service (e.g., 'twilio')
        self.phone_call_provider = data.get('phoneCallProvider')
        # Transport method for the call (e.g., 'sip')
        self.phone_call_transport = data.get('phoneCallTransport')
        # Timestamp when the call was created
        self.created_at = datetime.fromisoformat(data['createdAt'].rstrip('Z')) if data.get('createdAt') else None
        # Timestamp when the call was last updated
        self.updated_at = datetime.fromisoformat(data['updatedAt'].rstrip('Z')) if data.get('updatedAt') else None
        # Timestamp when the call started
        self.started_at = datetime.fromisoformat(data['startedAt'].rstrip('Z')) if data.get('startedAt') else None
        # Timestamp when the call ended
        self.ended_at = datetime.fromisoformat(data['endedAt'].rstrip('Z')) if data.get('endedAt') else None
        # Total cost of the call
        self.cost = data.get('cost')
        # Detailed breakdown of the call costs
        self.cost_breakdown = data.get('costBreakdown')
        # List of messages exchanged during the call
        self.messages = data.get('messages', [])
        # Artifacts generated during the call (e.g., recordings, transcripts)
        self.artifact = data.get('artifact', {})
        # Analysis of the call (e.g., summary, structured data)
        self.analysis = data.get('analysis', {})
        # Monitoring information for the call
        self.monitor = data.get('monitor', {})
        # Destination information for the call
        self.destination = data.get('destination', {})
        # Details of the assistant handling the call
        self.assistant = data.get('assistant', {})
        # Any overrides applied to the assistant for this specific call
        self.assistant_overrides = data.get('assistantOverrides', {})
        # Details of the squad associated with the call (if applicable)
        self.squad = data.get('squad', {})
        # Details of the phone number used for the call
        self.phone_number = data.get('phoneNumber', {})
        # Details of the customer associated with the call
        self.customer = data.get('customer', {})

    def __str__(self):
        return f"Call: {self.name} (ID: {self.id}, Status: {self.status})"


class CallManager(APIClient):
    def __init__(self):
        super().__init__()
        self.endpoint = "call"

    def create_call(self, name, assistant_id, **kwargs):
        payload = {
            "name": name,
            "assistantId": assistant_id,
            **kwargs
        }
        response = self.post(self.endpoint, payload)
        return Call(response)

    def get_call(self, call_id):
        response = self.get(f"{self.endpoint}/{call_id}")
        return Call(response)

    def list_calls(self):
        response = self.get(self.endpoint)
        return [Call(call_data) for call_data in response]

    def update_call(self, call_id, **kwargs):
        response = self.patch(f"{self.endpoint}/{call_id}", kwargs)
        return Call(response)

    def delete_call(self, call_id):
        return self.delete(f"{self.endpoint}/{call_id}")




class Assistant:
    def __init__(self, data):

        self.id = data['id']
        self.org_id = data['orgId']
        self.name = data['name']
        self.voice = data['voice']
        self.created_at = datetime.fromisoformat(data['createdAt'].rstrip('Z'))
        self.updated_at = datetime.fromisoformat(data['updatedAt'].rstrip('Z'))
        self.model = data['model']
        self.recording_enabled = data['recordingEnabled']
        self.first_message = data['firstMessage']
        self.transcriber = data['transcriber']
        self.silence_timeout_seconds = data['silenceTimeoutSeconds']
        self.client_messages = data['clientMessages']
        self.server_messages = data['serverMessages']
        self.end_call_phrases = data['endCallPhrases']
        self.hipaa_enabled = data['hipaaEnabled']
        self.max_duration_seconds = data['maxDurationSeconds']
        self.background_sound = data['backgroundSound']
        self.backchanneling_enabled = data['backchannelingEnabled']
        self.first_message_mode = data['firstMessageMode']
        self.voicemail_detection = data['voicemailDetection']
        self.background_denoising_enabled = data['backgroundDenoisingEnabled']
        self.model_output_in_messages_enabled = data['modelOutputInMessagesEnabled']
        self.is_server_url_secret_set = data['isServerUrlSecretSet']
        
        ## Call related init
        self.call_manager = CallManager()

    def create_call(self, name, **kwargs):
        return self.call_manager.create_call(name, self.id, **kwargs)
    
    def get_call(self, call_id):
        return self.call_manager.get_call(call_id)
    
    def list_calls(self):
        return self.call_manager.list_calls()
    
    def update_call(self, call_id, **kwargs):
        return self.call_manager.update_call(call_id, **kwargs)
    
    def delete_call(self, call_id):
        return self.call_manager.delete_call(call_id)
    
    
    
    @classmethod
    def from_json(cls, json_data):
        return cls(json_data)

    def to_django_model(self):
        return AssistantModel(
            id=self.id,
            org_id=self.org_id,
            name=self.name,
            voice=self.voice,
            created_at=self.created_at,
            updated_at=self.updated_at,
            model=self.model,
            recording_enabled=self.recording_enabled,
            first_message=self.first_message,
            transcriber=self.transcriber,
            silence_timeout_seconds=self.silence_timeout_seconds,
            client_messages=self.client_messages,
            server_messages=self.server_messages,
            end_call_phrases=self.end_call_phrases,
            hipaa_enabled=self.hipaa_enabled,
            max_duration_seconds=self.max_duration_seconds,
            background_sound=self.background_sound,
            backchanneling_enabled=self.backchanneling_enabled,
            first_message_mode=self.first_message_mode,
            voicemail_detection=self.voicemail_detection,
            background_denoising_enabled=self.background_denoising_enabled,
            model_output_in_messages_enabled=self.model_output_in_messages_enabled,
            is_server_url_secret_set=self.is_server_url_secret_set
        )

    def save_to_db(self):
        django_model = self.to_django_model()
        django_model.save()
        return django_model

    def __str__(self):
        return f"Assistant: {self.name} (ID: {self.id})"


class VAPIAssistant(APIClient):
    def __init__(self):
        super().__init__()
        self.endpoint = "assistant"

    def create_assistant(self, name, first_message, transcriber=None, model=None, voice=None, **kwargs):
        payload = {
            "name": name,
            "firstMessage": first_message,
            "transcriber": transcriber or DEFAULT_TRANSCRIBER_CONFIG,
            "model": model or DEFAULT_MODEL_CONFIG,
            "voice": voice or DEFAULT_VOICE_CONFIG,
            "firstMessageMode": kwargs.get("firstMessageMode", "assistant-speaks-first"),
            "recordingEnabled": kwargs.get("recordingEnabled", True),
            "hipaaEnabled": kwargs.get("hipaaEnabled", False),
            "clientMessages": kwargs.get("clientMessages", [
                "conversation-update", "function-call", "hang", "model-output",
                "speech-update", "status-update", "transcript", "tool-calls",
                "user-interrupted", "voice-input"
            ]),
            "serverMessages": kwargs.get("serverMessages", [
                "conversation-update", "end-of-call-report", "function-call",
                "hang", "speech-update", "status-update", "tool-calls",
                "transfer-destination-request", "user-interrupted"
            ]),
            "silenceTimeoutSeconds": kwargs.get("silenceTimeoutSeconds", 30),
            "maxDurationSeconds": kwargs.get("maxDurationSeconds", 600),
            "backgroundSound": kwargs.get("backgroundSound", "office"),
            "backchannelingEnabled": kwargs.get("backchannelingEnabled", False),
            "backgroundDenoisingEnabled": kwargs.get("backgroundDenoisingEnabled", False),
            "modelOutputInMessagesEnabled": kwargs.get("modelOutputInMessagesEnabled", False),
        }

        # Optional fields
        optional_fields = [
            "transportConfigurations", "voicemailDetection", "voicemailMessage",
            "endCallMessage", "endCallPhrases", "metadata", "serverUrl",
            "serverUrlSecret", "analysisPlan", "artifactPlan", "messagePlan",
            "startSpeakingPlan", "stopSpeakingPlan", "credentialIds"
        ]

        for field in optional_fields:
            if field in kwargs:
                payload[field] = kwargs[field]

        response = self.post(self.endpoint, payload)
        return Assistant(response)

    def get_assistant(self, assistant_id):
        response = self.get(f"{self.endpoint}/{assistant_id}")
        print(response)
        raise ValueError
        return Assistant(response)

    def update_assistant(self, assistant_id, **kwargs): 
        response = self.patch(f"{self.endpoint}/{assistant_id}", kwargs)
        return Assistant(response)

    def delete_assistant(self, assistant_id):
        return self.delete(f"{self.endpoint}/{assistant_id}")

    def list_assistants(self):
        response = self.get(self.endpoint)
        return [Assistant(assistant_data) for assistant_data in response]
    
    
    
    
    

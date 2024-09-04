from api.client import APIClient
from api.config import DEFAULT_TRANSCRIBER_CONFIG, DEFAULT_MODEL_CONFIG, DEFAULT_VOICE_CONFIG
import datetime
import json
       
from management.models import AssistantModel

from datetime import datetime

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
    
    
    
    
    

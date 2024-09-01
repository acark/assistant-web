from api.client import APIClient
from api.config import DEFAULT_TRANSCRIBER_CONFIG, DEFAULT_MODEL_CONFIG, DEFAULT_VOICE_CONFIG
import datetime
import json
       
from management.models import Assistant as DjangoAssistant
class Assistant:
    def __init__(self, data):
        self.id = data.get('id')
        self.org_id = data.get('orgId')
        self.name = data.get('name')
        self.voice = data.get('voice')
        self.created_at = datetime.fromisoformat(data.get('createdAt').rstrip('Z'))
        self.updated_at = datetime.fromisoformat(data.get('updatedAt').rstrip('Z'))
        self.model = data.get('model')
        self.recording_enabled = data.get('recordingEnabled')
        self.first_message = data.get('firstMessage')
        self.voicemail_message = data.get('voicemailMessage')
        self.end_call_message = data.get('endCallMessage')
        self.transcriber = data.get('transcriber')
        self.client_messages = data.get('clientMessages')
        self.server_messages = data.get('serverMessages')
        self.end_call_phrases = data.get('endCallPhrases')
        self.num_words_to_interrupt_assistant = data.get('numWordsToInterruptAssistant')
        self.background_sound = data.get('backgroundSound')
        self.is_server_url_secret_set = data.get('isServerUrlSecretSet')
    def __str__(self):
        return f"Assistant(id={self.id}, name={self.name})"        

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.__dict__, file, default=str, indent=4)
    def save_to_db(self):
        assistant_data = {
            'id': self.id,
            'org_id': self.org_id,
            'name': self.name,
            'voice': self.voice,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'model': self.model,
            'recording_enabled': self.recording_enabled,
            'first_message': self.first_message,
            'voicemail_message': self.voicemail_message,
            'end_call_message': self.end_call_message,
            'transcriber': self.transcriber,
            'client_messages': self.client_messages,
            'server_messages': self.server_messages,
            'end_call_phrases': self.end_call_phrases,
            'num_words_to_interrupt_assistant': self.num_words_to_interrupt_assistant,
            'background_sound': self.background_sound,
            'is_server_url_secret_set': self.is_server_url_secret_set}
        DjangoAssistant.objects.update_or_create(id=self.id, defaults=assistant_data)


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
            "recordingEnabled": kwargs.get("recordingEnabled", True),
            "voicemailMessage": kwargs.get("voicemailMessage", ""),
            "endCallMessage": kwargs.get("endCallMessage", ""),
            "clientMessages": kwargs.get("clientMessages", ["tool-calls", "tool-calls-result", "function-call"]),
            "serverMessages": kwargs.get("serverMessages", ["tool-calls", "function-call"]),
            "endCallPhrases": kwargs.get("endCallPhrases", []),
            "numWordsToInterruptAssistant": kwargs.get("numWordsToInterruptAssistant", 2),
            "backgroundSound": kwargs.get("backgroundSound", "office"),
        }
        
        # Only include serverUrl if it's provided and valid
        server_url = kwargs.get("serverUrl")
        if server_url and server_url.startswith("https://"):
            payload["serverUrl"] = server_url

        return self.post(self.endpoint, payload)
    
    def get_assistant(self, assistant_id):
        response = self.get(f"{self.endpoint}/{assistant_id}")
        return Assistant(response)


    def update_assistant(self, assistant_id, **kwargs):
        response = self.put(f"{self.endpoint}/{assistant_id}", kwargs)
        return Assistant(response)

    def delete_assistant(self, assistant_id):
        return self.delete(f"{self.endpoint}/{assistant_id}")

    def list_assistants(self):
        response = self.get(self.endpoint)
        return [Assistant(assistant_data) for assistant_data in response]
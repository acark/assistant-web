from openai import OpenAI
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import openai
from django.conf import settings

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.system_prompt = ""
        self.assistant_prompt = {}
        self.model = "gpt-3.5-turbo"

    def set_system_prompt(self, prompt: str):
        self.system_prompt = prompt

    def set_assistant_prompt(self, prompt: Dict[str, Any]):
        self.assistant_prompt = prompt

    def set_model(self, model: str):
        self.model = model

    def create_chat_completion(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return completion

    def extract_information(self, user_content: str) -> Dict[str, Any]:
        current_time = datetime.now().isoformat()
        messages = [
            {"role": "system", "content": f"{self.system_prompt}\nCurrent date and time: {current_time}"},
            {"role": "assistant", "content": json.dumps(self.assistant_prompt)},
            {"role": "user", "content": user_content}
        ]
        
        response = self.create_chat_completion(messages)
        
        extracted_info = response.choices[0].message.content
        
        try:
            return json.loads(extracted_info)  # Attempt to parse as JSON
        except json.JSONDecodeError:
            return {"raw_response": extracted_info}  # Return raw text if not JSON

class InformationExtractor:
    def __init__(self, system_prompt: str, assistant_prompt: Dict[str, Any], model: Optional[str] = None):
        self.client = OpenAIClient()
        self.client.set_system_prompt(system_prompt)
        self.client.set_assistant_prompt(assistant_prompt)
        if model:
            self.client.set_model(model)

    def extract(self, user_content: str) -> Dict[str, Any]:
        return self.client.extract_information(user_content)


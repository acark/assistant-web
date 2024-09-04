import os
import django
import logging
import json
from requests.exceptions import RequestException

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from vapi_api.assistant import VAPIAssistant
from django.conf import settings

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_create_assistant():
    vapi = VAPIAssistant()
    try:
        assistant = vapi.create_assistant(
            name="Test Assistantasd",
            first_message="Hello, how can I assist you today?",
            transcriber={
                "provider": "deepgram",
                "model": "nova-2",
                "language": "en",
                "smartFormat": False,
                "endpointing": 500
            },
            model={
                "provider": "openai",
                "model": "chat",
                "temperature": 0.7,
                "maxTokens": 1000,
                "emotionRecognitionEnabled": True,
                "numFastTurns": 0
            },
            voice={
                "provider": "playht",
                "voiceId": "jennifer"
            },
            backgroundSound="office",
            silenceTimeoutSeconds=30,
            maxDurationSeconds=600,
            endCallPhrases=["Goodbye", "Thank you for calling"],
            voicemailDetection={
                "enabled": True,
                "provider": "twilio"
            }
        )
        logger.info("Assistant created successfully:")
        assistant.save_to_db()
    except RequestException as e:
        logger.error(f"Error creating assistant: {str(e)}")
        if e.response is not None:
            logger.error(f"Response status code: {e.response.status_code}")
            logger.error(f"Response content: {e.response.text}")
        logger.error(f"Request URL: {e.request.url}")
        logger.error(f"Request headers: {e.request.headers}")
        logger.error(f"Request body: {e.request.body}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    logger.info(f"Using API URL: {settings.VAPI_API_URL}")
    test_create_assistant()
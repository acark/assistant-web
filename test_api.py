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
    assistant = VAPIAssistant()
    try:
        response = assistant.create_assistant(
            name="Test Assistant",
            first_message="Ben Test Assistant, Size nasıl yardımcı olabilirim?",
            transcriber={"model": "nova-2-general", "language": "tr", "provider": "deepgram"},
            model={
                "model": "gpt-4o",
                "provider": "openai",
                "emotionRecognitionEnabled": True,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant."
                    }
                ]
            },
            voice={"voiceId": "onyx", "provider": "openai"},
            endCallPhrases=["Gorusuruz."]
        )
        logger.info("Assistant created successfully:")
        logger.info(json.dumps(response, indent=2))
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


def test_update_assisant():
    
    assistant = VAPIAssistant().get_assistant()
    


if __name__ == "__main__":
    logger.info(f"Using API URL: {settings.VAPI_API_URL}")
    test_create_assistant()
    test_update_assisant()
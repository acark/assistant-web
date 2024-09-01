

## This should be taken from front-side
DEFAULT_TRANSCRIBER_CONFIG = {
    "provider": "deepgram",
    "model": "nova-2",
    "language": "bg",
    "smartFormat": False,
    "endpointing": 255
}

DEFAULT_MODEL_CONFIG = {
    "model": "gpt-4o",
    "provider": "openai",
    "emotionRecognitionEnabled": True,
    "toolIds": [],  # This can be populated as needed
    "messages": [
        {
            "role": "system",
            "content": "Default system message content"
        }
    ]
}

DEFAULT_VOICE_CONFIG = {
    "voiceId": "onyx",
    "provider": "openai"
}
DEFAULT_TRANSCRIBER_CONFIG = {
    "model": "nova-2-general",
    "language": "tr",
    "provider": "deepgram"
}

DEFAULT_MODEL_CONFIG = {
    "model": "gpt-4o",
    "provider": "openai",
    "emotionRecognitionEnabled": True,
    "toolIds": [],  # This can be populated as needed
    "messages": [
        {
            "role": "system",
            "content": "!!!Promt!!!"
        }
    ]
}

DEFAULT_VOICE_CONFIG = {
    "voiceId": "onyx",
    "provider": "openai"
}
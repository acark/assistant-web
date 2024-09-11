import os
import django
from django.conf import settings
import sys
# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from openai_api.openai_client import InformationExtractor, OpenAIClient

class TestOpenAIClient(unittest.TestCase):

    def setUp(self):
        self.extractor = InformationExtractor(
            system_prompt="You are an AI assistant that extracts and interprets date and time information from user input. Please convert relative time expressions to absolute dates and times based on the current date and time provided.",
            assistant_prompt={
                "task": "Extract booking date and time",
                "format": {
                    "booking_datetime": "YYYY-MM-DD HH:MM:SS"
                }
            },
            model="gpt-3.5-turbo"
        )

    @patch('openai_client.OpenAIClient.create_chat_completion')
    def test_extract_next_friday(self, mock_create_chat_completion):
        # Set up the mock response
        mock_response = {
            'choices': [
                {
                    'message': {
                        'content': '{"booking_datetime": "2023-05-05 18:00:00"}'
                    }
                }
            ]
        }
        mock_create_chat_completion.return_value = mock_response

        # Set a fixed current date for testing
        current_date = datetime(2023, 5, 1)  # A Monday
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = current_date

            # Test the extractor
            result = self.extractor.extract("Book an appointment for next Friday at 6PM")

        self.assertEqual(result, {"booking_datetime": "2023-05-05 18:00:00"})

    @patch('openai_client.OpenAIClient.create_chat_completion')
    def test_extract_tomorrow(self, mock_create_chat_completion):
        # Set up the mock response
        mock_response = {
            'choices': [
                {
                    'message': {
                        'content': '{"booking_datetime": "2023-05-02 10:00:00"}'
                    }
                }
            ]
        }
        mock_create_chat_completion.return_value = mock_response

        # Set a fixed current date for testing
        current_date = datetime(2023, 5, 1)  # A Monday
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = current_date

            # Test the extractor
            result = self.extractor.extract("Schedule a meeting for tomorrow at 10AM")

        self.assertEqual(result, {"booking_datetime": "2023-05-02 10:00:00"})

    @patch('openai_client.OpenAIClient.create_chat_completion')
    def test_extract_next_month(self, mock_create_chat_completion):
        # Set up the mock response
        mock_response = {
            'choices': [
                {
                    'message': {
                        'content': '{"booking_datetime": "2023-06-15 14:30:00"}'
                    }
                }
            ]
        }
        mock_create_chat_completion.return_value = mock_response

        # Set a fixed current date for testing
        current_date = datetime(2023, 5, 15)
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = current_date

            # Test the extractor
            result = self.extractor.extract("Let's have a review meeting next month on the 15th at 2:30PM")

        self.assertEqual(result, {"booking_datetime": "2023-06-15 14:30:00"})

if __name__ == '__main__':
    unittest.main()

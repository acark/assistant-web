import unittest
from unittest.mock import Mock, patch
from datetime import datetime
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
from vapi_api.assistant import Call, CallManager

class TestCallManager(unittest.TestCase):

    def setUp(self):
        self.call_manager = CallManager()

    @patch('vapi_api.assistant.APIClient.post')
    def test_create_call(self, mock_post):
        mock_response = {
            'id': '123',
            'name': 'Test Call',
            'assistantId': 'assistant_123',
            'status': 'queued',
            'createdAt': '2023-04-01T12:00:00Z'
        }
        mock_post.return_value = mock_response

        call = self.call_manager.create_call('Test Call', 'assistant_123')

        self.assertIsInstance(call, Call)
        self.assertEqual(call.id, '123')
        self.assertEqual(call.name, 'Test Call')
        self.assertEqual(call.assistant_id, 'assistant_123')
        self.assertEqual(call.status, 'queued')
        self.assertEqual(call.created_at, datetime(2023, 4, 1, 12, 0))

    @patch('vapi_api.assistant.APIClient.get')
    def test_get_call(self, mock_get):
        mock_response = {
            'id': '456',
            'name': 'Existing Call',
            'status': 'in-progress'
        }
        mock_get.return_value = mock_response

        call = self.call_manager.get_call('456')

        self.assertIsInstance(call, Call)
        self.assertEqual(call.id, '456')
        self.assertEqual(call.name, 'Existing Call')
        self.assertEqual(call.status, 'in-progress')

    @patch('vapi_api.assistant.APIClient.get')
    def test_list_calls(self, mock_get):
        mock_response = [
            {'id': '1', 'name': 'Call 1'},
            {'id': '2', 'name': 'Call 2'}
        ]
        mock_get.return_value = mock_response

        calls = self.call_manager.list_calls()

        self.assertEqual(len(calls), 2)
        self.assertIsInstance(calls[0], Call)
        self.assertEqual(calls[0].id, '1')
        self.assertEqual(calls[1].name, 'Call 2')

    @patch('vapi_api.assistant.APIClient.patch')
    def test_update_call(self, mock_patch):
        mock_response = {
            'id': '789',
            'name': 'Updated Call',
            'status': 'completed'
        }
        mock_patch.return_value = mock_response

        call = self.call_manager.update_call('789', name='Updated Call', status='completed')

        self.assertIsInstance(call, Call)
        self.assertEqual(call.id, '789')
        self.assertEqual(call.name, 'Updated Call')
        self.assertEqual(call.status, 'completed')

    @patch('vapi_api.assistant.APIClient.delete')
    def test_delete_call(self, mock_delete):
        mock_delete.return_value = None

        result = self.call_manager.delete_call('101')

        self.assertIsNone(result)
        mock_delete.assert_called_once_with('call/101')

class TestCall(unittest.TestCase):

    def test_call_initialization(self):
        call_data = {
            'id': 'call_123',
            'orgId': 'org_456',
            'name': 'Test Call',
            'type': 'inboundPhoneCall',
            'assistantId': 'assistant_789',
            'status': 'completed',
            'createdAt': '2023-04-01T12:00:00Z',
            'endedAt': '2023-04-01T12:05:00Z',
            'cost': 1.23
        }

        call = Call(call_data)

        self.assertEqual(call.id, 'call_123')
        self.assertEqual(call.org_id, 'org_456')
        self.assertEqual(call.name, 'Test Call')
        self.assertEqual(call.type, 'inboundPhoneCall')
        self.assertEqual(call.assistant_id, 'assistant_789')
        self.assertEqual(call.status, 'completed')
        self.assertEqual(call.created_at, datetime(2023, 4, 1, 12, 0))
        self.assertEqual(call.ended_at, datetime(2023, 4, 1, 12, 5))
        self.assertEqual(call.cost, 1.23)

    def test_call_str_representation(self):
        call = Call({'id': 'call_123', 'name': 'Test Call', 'status': 'in-progress'})
        self.assertEqual(str(call), "Call: Test Call (ID: call_123, Status: in-progress)")

if __name__ == '__main__':
    unittest.main()
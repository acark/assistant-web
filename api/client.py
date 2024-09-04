import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self):
        self.base_url = settings.VAPI_API_URL.rstrip('/')  # Remove trailing slash if present
        self.headers = {
            "Authorization": f"Bearer {settings.VAPI_API_TOKEN}",
            "Content-Type": "application/json"
        }

    def _make_request(self, method, endpoint, payload=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.debug(f"Sending {method} request to {url}")
        if payload:
            logger.debug(f"Request payload: {payload}")

        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers)
            elif method == 'POST':
                response = requests.post(url, json=payload, headers=self.headers)
            elif method == 'PUT':
                response = requests.put(url, json=payload, headers=self.headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            logger.debug(f"Response status code: {response.status_code}")
            logger.debug(f"Response content: {response.text}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            if e.response is not None:
                logger.error(f"Response status code: {e.response.status_code}")
                logger.error(f"Response content: {e.response.text}")
            raise

    def get(self, endpoint):
        return self._make_request('GET', endpoint)

    def post(self, endpoint, payload):
        return self._make_request('POST', endpoint, payload)

    def put(self, endpoint, payload):
        return self._make_request('PUT', endpoint, payload)

    def delete(self, endpoint):
        return self._make_request('DELETE', endpoint)
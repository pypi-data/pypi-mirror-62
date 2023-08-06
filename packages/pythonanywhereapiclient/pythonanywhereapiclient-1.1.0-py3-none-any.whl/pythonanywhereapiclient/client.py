import requests

from urllib.parse import urljoin

from pythonanywhereapiclient.utils import getenv


class Client:
    def __init__(self, host=None, token=None, user=None):
        self.host = host or getenv('API_HOST')
        self.token = token or getenv('API_TOKEN')
        self.user = user or getenv('API_USER')
        self.base_url = f'https://{self.host}/api/v0/user/{self.user}/'.lower()

    def _construct_endpoint_url(self, endpoint):
        return urljoin(self.base_url, endpoint)

    def _headers(self):
        return {'Authorization': f'Token {self.token}'}

    def delete(self, endpoint):
        return requests.delete(
            self._construct_endpoint_url(endpoint),
            headers=self._headers()
        )

    def get(self, endpoint):
        return requests.get(
            self._construct_endpoint_url(endpoint),
            headers=self._headers()
        )

    def patch(self, endpoint, data=None):
        return requests.patch(
            self._construct_endpoint_url(endpoint),
            headers=self._headers(),
            data=data
        )

    def post(self, endpoint, data=None, files=None):
        return requests.post(
            self._construct_endpoint_url(endpoint),
            headers=self._headers(),
            data=data,
            files=files
        )

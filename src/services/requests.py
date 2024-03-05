import requests
from requests.exceptions import RequestException
from ..exceptions import BadRequestToExternalService

class RequestsService:
    def __init__(self, base_url=None, api_key=None):
        """
        Initialize the RequestHandler with an optional base URL.
        :param base_url: Base URL to which the endpoints will be appended.
        """
        self.base_url = base_url
        self.default_headers = {}
        self.token = None
        if api_key:
            self.authenticate(api_key)
        
        
    def authenticate(self, api_key):
        """
        Authenticate the user sets the access token
        and sets the default headers.
        :param api_key: API key for authentication.
        :return: Access token.
        """
        response = self.send_post_request('/auth/token', json={'api_key': api_key})
        if response and response.status_code == 200:
            res = response.json()
            self.token = res['access_token']
            self.default_headers['Authorization'] = f"Bearer {self.token}"

    def _full_url(self, endpoint):
        """
        Construct the full URL by combining the base URL with the endpoint.
        :param endpoint: The specific endpoint for the request.
        :return: Full URL.
        """
        return f"{self.base_url}{endpoint}" if self.base_url else endpoint

    def send_get_request(self, endpoint, params=None):
        """
        Send a GET request to the specified endpoint.
        :param endpoint: Endpoint for the GET request.
        :param params: Optional parameters for the request.
        :return: Response object or None in case of an exception.
        """
        try:
            response = requests.get(self._full_url(endpoint), params=params, headers=self.default_headers)
            response.raise_for_status()  # Raise an exception for HTTP error statuses
            return response
        except RequestException as e:
            print(f"Error during GET request: {e}")
            raise BadRequestToExternalService(str(e))

    def send_post_request(self, endpoint, data=None, json=None):
        """
        Send a POST request to the specified endpoint.
        :param endpoint: Endpoint for the POST request.
        :param data: Data to be sent in the form of form-data.
        :param json: Data to be sent in JSON format.
        :return: Response object or None in case of an exception.
        """
        try:
            response = requests.post(self._full_url(endpoint), data=data, json=json, headers=self.default_headers)
            response.raise_for_status()
            return response
        except RequestException as e:
            print(f"Error during POST request: {e}")
            raise BadRequestToExternalService(str(e))
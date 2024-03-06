#https://github.com/samamorgan/helpjuice/blob/master/helpjuice/client.py
import requests
from requests.exceptions import RequestException, ConnectionError
from ..exceptions import BadRequestToExternalService, CannotConnectToExternalService, AuthenticationFailed
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry # type: ignore

class HttpClient:
    def __init__(self, base_url, api_key, auth_endpoint='/auth/token'):
        self.base_url = base_url
        self.api_key = api_key
        self.auth_endpoint = auth_endpoint
        self.token = None
        self.session = requests.Session()
        self.configure_retries()
    
    def _full_url(self, endpoint):
        """
        Construct the full URL by combining the base URL with the endpoint.
        :param endpoint: The specific endpoint for the request.
        :return: Full URL.
        """
        return f"{self.base_url}{endpoint}" if self.base_url else endpoint

    def authenticate(self):
        try:
            response = self.session.post(self._full_url(self.auth_endpoint), json={"api_key": self.api_key})
            if response.status_code == 200:
                self.token = response.json().get('access_token')
                self.session.headers.update({'Authorization': f'Bearer {self.token}'})
            else:
                raise AuthenticationFailed
        except ConnectionError as e:
            raise CannotConnectToExternalService(str(e))

    def configure_retries(self, total_retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504)):
        retry_strategy = Retry(
            total=total_retries,
            read=total_retries,
            connect=total_retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def get(self, url):
        try:
            if not self.token:
                self.authenticate()
            response = self.session.get(self._full_url(url))
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            raise BadRequestToExternalService(str(e))

    def post(self, url, data):
        try:
            if not self.token:
                self.authenticate()
            response = self.session.post(self._full_url(url), json=data)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            raise BadRequestToExternalService(str(e)+response.text)

# class HttpClient:
#     def __init__(self, base_url=None, api_key=None):
#         """
#         Initialize the RequestHandler with an optional base URL.
#         :param base_url: Base URL to which the endpoints will be appended.
#         """
#         self.base_url = base_url
#         self.default_headers = {}
#         self.token = None
#         if api_key:
#             self.authenticate(api_key)
        
        
#     def authenticate(self, api_key):
#         """
#         Authenticate the user sets the access token
#         and sets the default headers.
#         :param api_key: API key for authentication.
#         :return: Access token.
#         """
#         try:
#             response = self.send_post_request('/auth/token', json={'api_key': api_key})
#             if response and response.status_code == 200:
#                 res = response.json()
#                 self.token = res['access_token']
#                 self.default_headers['Authorization'] = f"Bearer {self.token}"
#         except CannotConnectToExternalService as e:
#             print(f"cannot connect to external service {e}")
#             #we dont raise as this is not a critical error
        

#     def _full_url(self, endpoint):
#         """
#         Construct the full URL by combining the base URL with the endpoint.
#         :param endpoint: The specific endpoint for the request.
#         :return: Full URL.
#         """
#         return f"{self.base_url}{endpoint}" if self.base_url else endpoint

#     def send_get_request(self, endpoint, params=None):
#         """
#         Send a GET request to the specified endpoint.
#         :param endpoint: Endpoint for the GET request.
#         :param params: Optional parameters for the request.
#         :return: Response object or None in case of an exception.
#         """
#         try:
#             response = requests.get(self._full_url(endpoint), params=params, headers=self.default_headers)
#             response.raise_for_status()  # Raise an exception for HTTP error statuses
#             return response
#         except RequestException as e:
#             print(f"Error during GET request: {e}")
#             raise BadRequestToExternalService(str(e))

#     def send_post_request(self, endpoint, data=None, json=None):
#         """
#         Send a POST request to the specified endpoint.
#         :param endpoint: Endpoint for the POST request.
#         :param data: Data to be sent in the form of form-data.
#         :param json: Data to be sent in JSON format.
#         :return: Response object or None in case of an exception.
#         """
#         try:
#             response = requests.post(self._full_url(endpoint), data=data, json=json, headers=self.default_headers)
#             response.raise_for_status()
#             return response
#         except RequestException as e:
#             print(f"Error during POST request: {e}")
#             raise BadRequestToExternalService(str(e))
#https://github.com/samamorgan/helpjuice/blob/master/helpjuice/client.py
import requests
from requests.exceptions import RequestException, ConnectionError
from ..exceptions import CannotConnectToExternalService, AuthenticationFailed
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry # type: ignore
import logging

class HttpClient:
    def __init__(self, base_url, api_key, auth_endpoint='/auth/token'):
        self.logger = logging.getLogger(__name__)
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
            self.logger.warning(f"Request failed: {e}")
            return response.json()

    def post(self, url, data):
        try:
            if not self.token:
                self.authenticate()
            response = self.session.post(self._full_url(url), json=data)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            self.logger.warning(f"Request failed: {e}")
            return response.json()
        
    def put(self, url, data):
        try:
            if not self.token:
                self.authenticate()
            response = self.session.put(self._full_url(url), json=data)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            self.logger.warning(f"Request failed: {e}")
            return response.json()

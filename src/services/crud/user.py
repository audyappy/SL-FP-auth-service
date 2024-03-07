from typing import Any
import os
from werkzeug.security import generate_password_hash
from requests.exceptions import RequestException

from .base import CRUDService
from ..auth import AuthService
from ..http_client import HttpClient
from ...models import User
from ...schemas import user_schema


class UserService(CRUDService):
    def __init__(self):
        super().__init__(User, user_schema)
        self.auth_service = AuthService()
        
        backend_service_url = os.environ.get('BACKEND_SERVICE_URL')
        backend_service_api_key = os.environ.get('BACKEND_SERVICE_API_KEY')
        self.backend_requests_service = HttpClient(backend_service_url, backend_service_api_key)
        
    def create_or_update_user_in_backend(self, data)->Any:
        """
        creates a new user in backend service if user does not exist
        """
        username = data['username']
        email = data['email']
        json_data = {'username': username, 'email': email}
        
        res =self.backend_requests_service.post('/users/', data=json_data)

    
    def register(self, data)->Any:
        """
        creates a new user both in auth and backend services and returns a token
        returns (user, token) tuple
        """
        self.create_or_update_user_in_backend(data)
        user = self.create(data)
        token = self.auth_service.get_user_token(user)
        return user, token
    
    def create(self, data)->Any:
        data['password_hash'] = generate_password_hash(data['password'])
        return super().create(data)
        

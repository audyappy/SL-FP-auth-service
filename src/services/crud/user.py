from typing import Any
import os
from werkzeug.security import generate_password_hash

from .base import CRUDService
from ..auth import AuthService
from ..requests import RequestsService
from ...models import User
from ...schemas import user_schema
from ...exceptions import BadRequestToExternalService

class UserService(CRUDService):
    def __init__(self):
        super().__init__(User, user_schema)
        self.auth_service = AuthService()
        
        backend_service_url = os.environ.get('BACKEND_SERVICE_URL')
        backend_service_api_key = os.environ.get('BACKEND_SERVICE_API_KEY')
        self.backend_requests_service = RequestsService(backend_service_url, backend_service_api_key)
        
    def create_user_in_backend(self, data)->Any:
        """
        creates a new user in backend service
        """
        username = data['username']
        email = data['email']
        json_data = {'username': username, 'email': email}
        self.backend_requests_service.send_post_request('/users/', json=json_data)

    
    def register(self, data)->Any:
        """
        creates a new user both in auth and backend services and returns a token
        returns (user, token) tuple
        """
        user = self.create(data)
        token = self.auth_service.get_user_token(user)
        self.create_user_in_backend(data)
        return user, token
    
    def create(self, data)->Any:
        data['password_hash'] = generate_password_hash(data['password'])
        return super().create(data)
        

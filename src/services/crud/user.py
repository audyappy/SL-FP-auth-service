from typing import Any
from .base import CRUDService
from ..auth import AuthService
from ...models import User
from ...schemas import user_schema
from werkzeug.security import generate_password_hash

class UserService(CRUDService):
    def __init__(self):
        super().__init__(User, user_schema)
        self.auth_service = AuthService()
        
    
    def register(self, data)->Any:
        """
        returns (user, token) tuple
        """
        user = self.create(data)
        token = self.auth_service.get_user_token(user)
        return user, token
    
    def create(self, data)->Any:
        data['password_hash'] = generate_password_hash(data['password'])
        return super().create(data)
        

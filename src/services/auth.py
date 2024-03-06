from flask_jwt_extended import create_access_token
import os
from ..exceptions import UnauthorizedException, UserNotFound, InvalidPassword
from ..models import User

api_key = os.environ.get('API_KEY')

class AuthService:
    def __init__(self, api_key=api_key):
        self.api_key = api_key
        
    def api_authenticate(self, data):
        """
        used to authenticate with api_key (between services)
        returns access token if api_key_in is equal to the api_key
        throws UnauthorizedException if api_key_in is not equal to the api_key
        """
        api_key_in = data['api_key']
        if api_key_in != self.api_key:
            raise UnauthorizedException('Api key is invalid')
        return create_access_token(identity=api_key_in, additional_claims={'roles': ['api', 'user']})
    
    def get_user_token(self, user:User):
        """
        used to get access token for user
        """
        return create_access_token(identity=user.id, additional_claims={'roles': ['user']})
    
    
    def user_login(self, data):
        """
        returns (user, token) tuple
        """
        username, password = data['username'], data['password']
        user = User.query.filter_by(username=username).first()
        if user is None:
            raise UserNotFound
        if not user.check_password(password):
            raise InvalidPassword
        
        token = self.get_user_token(user)
        return user, token

        
        
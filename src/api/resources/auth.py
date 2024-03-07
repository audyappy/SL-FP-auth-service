from flask import request
from flask_restx import Resource, Namespace, fields
import os
from flask_jwt_extended import create_access_token

from ...services.auth import AuthService
from ...services.crud import UserService
from ...schemas import user_schema, users_schema

api = Namespace('auth', description='Operations related to authentication')

login_model = api.model('login', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

register_model = api.model('register', {
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

token_model = api.model('token', {
        'api_key': fields.String(required=True)
    })

user_service = UserService()
auth_service = AuthService()

@api.route('/login')
# @api.response(400, 'Bad request')
@api.response(200, 'Login successful.')
@api.response(401, 'invalid password')
@api.response(404, 'User not found')
class LoginResource(Resource):
    @api.expect(login_model, validate=True)
    def post(self):
        user, token = auth_service.user_login(request.json)
        data = user_schema.dump(user)
        assert isinstance(data, dict)
        data['token'] = token
        return data, 200
    
@api.route('/register')
@api.response(400, 'Bad request')
@api.response(200, 'User successfully created.')
class RegisterResource(Resource):
    @api.expect(register_model, validate=True)
    def post(self):
        user, token = user_service.register(request.json)
        data = user_schema.dump(user)
        assert isinstance(data, dict)
        data['token'] = token
        return data, 200
    


@api.route('/token')
@api.response(400, 'Bad request')
@api.response(401, 'Api key is invalid')
@api.response(200, 'Access token successfully created.')
class TokenResource(Resource):
    @api.expect(token_model, validate=True)
    def post(self):
        token = auth_service.api_authenticate(request.json)
        return {'access_token': token,
        'header': f'Bearer {token}'
        }, 200

        


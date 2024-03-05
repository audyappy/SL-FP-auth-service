from flask_marshmallow import Marshmallow
from marshmallow import fields, validates, ValidationError
from .models import User
from re import match

ma = Marshmallow()

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True 
        
    password = fields.String(load_only=True, required=True)
    password_hash = fields.String(load_only=True)
    
    @validates('password')
    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        
    @validates('username')
    def validate_username(self, value):
        if len(value) < 3 or len(value) > 20:
            raise ValidationError("Username must be between 3 and 20 characters long.")
        if not match(r'^[a-zA-Z0-9_]+$', value):
            raise ValidationError("Username must contain only letters, numbers and underscores.")
        
    @validates('email')
    def validate_email(self, value):
        if not match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value):
            raise ValidationError("Invalid email address.")
    


# Initialize schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
from flask import Flask, jsonify, request
import os
import dotenv
from flask_restx import Api
from flask_jwt_extended import JWTManager
from marshmallow.exceptions import ValidationError

from .models import db
from .utils import set_db_uri
from .api.namespaces import add_namespace
from .exceptions import ServiceException

dotenv.load_dotenv()

app = Flask(__name__)
app.config['ERROR_404_HELP'] = False
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']

jwt = JWTManager(app)

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
api = Api(app, version='1.0', title='Authentication API',
          description='Authentication API for demo shop app', authorizations=authorizations)
add_namespace(api)
        
set_db_uri(app, os.environ['DATABASE_FILE_NAME'])

@app.errorhandler(ServiceException)
def handle_service_exception(error):
    """Handle ServiceException and its subclasses."""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(ValidationError)
def handle_validation_error(error):
    """Handle marshmallow ValidationError."""
    response = jsonify({'message': error.messages})
    response.status_code = 400
    return response

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/healthz')
def healthz():
    return "Healthy", 200
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)

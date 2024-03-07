import os
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
import logging



def set_db_uri(app, db_file_name):
    logger = logging.getLogger(__name__)
    if os.environ.get('SQLALCHEMY_DATABASE_URI'):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    else:
        src_dir = os.path.abspath(os.path.dirname(__file__))
        project_dir = os.path.dirname(src_dir)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(project_dir, 'data', db_file_name)
    logger.info(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
def create_directories():
    """
    creates data and logs directories if they don't exist
    """
    data_dir = 'data'
    logs_dir = 'logs'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
def requires_roles(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if any(role in claims.get("roles", []) for role in roles):
                return fn(*args, **kwargs)
            else:
                return jsonify({"msg": f"Insufficient permissions, {roles} required"}), 403
        return decorator
    return wrapper
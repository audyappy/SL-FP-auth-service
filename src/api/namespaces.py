from flask_restx import Api
from .resources.auth import api as auth_ns

def add_namespace(api:Api):
    api.add_namespace(auth_ns)
    
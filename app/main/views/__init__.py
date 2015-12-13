from app import api
from .auth import Auth


api.add_resource(Auth, "/login", endpoint="login")

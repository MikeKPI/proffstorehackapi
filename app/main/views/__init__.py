from app import api
from .auth import Auth
from project import Project, ProjectList

api.add_resource(Auth, "/login", endpoint="login")
api.add_resource(ProjectList, "/projects", endpoint="project")
api.add_resource(Project, "/projects/<string:id>", endpoint="project")

from app import api
from .auth import Auth
from project import Project, ProjectList
from task import Task, TaskList

api.add_resource(Auth, "/login", endpoint="login")
api.add_resource(ProjectList, "/projects", endpoint="project")
api.add_resource(Project, "/projects/<string:id>", endpoint="project")

api.add_resource(TaskList, "/tasks", endpoint="task")
api.add_resource(Task, "/tasks/<string:id>", endpoint="task")

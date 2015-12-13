from flask_restful import Resource
from .auth import login_required

class Task(Resource):

    @login_required
    def get(self):
        pass

    @login_required
    def post(self):
        pass

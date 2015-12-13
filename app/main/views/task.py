from flask_restful import Resource


class Task(Resource):

    @login_required
    def get(self):
        pass

    @login_required
    def post(self):
        pass

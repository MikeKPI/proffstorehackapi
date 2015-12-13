from flask_restful import Resource


class Project(Resource):

    @login_required
    def get(self):
        pass

    @login_required
    def post(self):
        pass

    @login_required
    def delete(self):
        pass

    @login_required
    def put(self):
        pass

from app.main.views import app, api
from flask import g, redirect, url_for, session
from flask_restful import Resource


def login_required(f):
    if g.user is None:
        return redirect(url_for("login"))


def require_roles():
    "http://flask.pocoo.org/snippets/98/ ?"
    pass


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


class Task(Resource):

    @login_required
    def get(self):
        pass

    @login_required
    def post(self):
        pass


class Auth(Resource):

    def get(self):
        pass


api.add_resource(Auth, "/login", endpoint="login")


if __name__ == "__main__":
    app.run(port=8080)
from flask_restful import Resource, fields, marshal_with, reqparse, abort
from sqlalchemy import and_
from .auth import login_required
from db import session
from app.models import Project, User
from flask import g

project_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "url": fields.Url('project', absolute=True)
}

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('description', type=str)


class Project(Resource):
    decorators = [login_required]

    @marshal_with(project_fields)
    def get(self, id):
        project = session.query(Project).filter(Project.id == id).first()
        if not project:
            return abort(404, message="Project does not exist")
        return project

    def delete(self, id):
        project = session.query(Project).filter(and_(Project.id == id,
                                                     Project.owner_id == g.user['id'])).first()
        if not project:
            return abort(403, message="Project does not exist or you do not have access")
        session.delete(project)
        session.commit()
        return {}, 204

    @marshal_with(project_fields)
    def put(self, id):
        parsed = parser.parse_args()
        project = session.query(Project).filter(and_(Project.id == id,
                                                     Project.owner_id == g.user['id'])).first()
        if not project:
            return abort(403, message="Project does not exist or you do not have access")
        project.name = parsed['name']
        project.description = parsed['description']
        session.add(project)
        session.commit()
        return project, 201


class ProjectList(Resource):
    decorators = [login_required]

    @marshal_with(project_fields)
    def get(self):
        projects = session.query(Project).all()
        return projects

    @marshal_with(project_fields)
    def post(self):
        parsed = parser.parse_args()
        user_id = session.query(User).filter(User.id == g.user['id']).first()
        project = Project(name=parsed['name'], description=parsed['description'], owner_id=user_id)
        session.add(project)
        session.commit()
        return project, 201

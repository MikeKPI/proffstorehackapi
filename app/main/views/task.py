from flask_restful import Resource, marshal_with, fields, abort, reqparse
from app import db
from sqlalchemy import and_
from flask import g
from app.models import Task, User, Project
from .auth import login_required

task_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "url": fields.Url('task', absolute=True)
}

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('description', type=str)
parser.add_argument('project_id', type=int)


class Task(Resource):
    decorators = [login_required]

    @marshal_with(task_fields)
    def get(self, id):
        task = db.session.query(Task).filter(Task.id == id).first()
        if not task:
            return abort(404, message="Task does not exist")
        return task

    def delete(self, id):
        user_id = db.session.query(User).filter(User.id == g.user['id']).first()
        task = db.session.query(Task).filter(Task.id == id).first()
        if not task:
            return abort(403, message="Task does not exist or you do not have access")
        db.session.delete(task)
        db.session.commit()
        return {}, 204

    @marshal_with(task_fields)
    def put(self, id):
        parsed = parser.parse_args()
        task = db.session.query(Task).filter(Task.id == id).first()
        if not task:
            return abort(403, message="Task does not exist or you do not have access")
        task.name = parsed['name']
        task.description = parsed['description']
        db.session.add(task)
        db.session.commit()
        return task, 201


class TaskList(Resource):
    decorators = [login_required]

    @marshal_with(task_fields)
    def get(self):
        tasks = db.session.query(Task).all()
        return tasks

    @marshal_with(task_fields)
    def post(self):
        parsed = parser.parse_args()
        # user_id = db.session.query(User).filter(User.id == g.user['id']).first()
        task = Task(name=parsed['name'], description=parsed['description'], project_id=parsed['project_id'])
        project_tasks = Project.tasks(parsed['project_id'], task.id)
        db.session.add(project_tasks)
        db.session.add(task)
        db.session.commit()
        return task, 201

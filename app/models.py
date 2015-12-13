from app import db

projects_users = db.Table('projects_users', db.Base.metadata,
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

users_tasks = db.Table('users_tasks', db.Base.metadata,
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

project_tasks = db.Table('project_tasks', db.Base.metadata,
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id')),
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'))
)


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(1024))
    owner_id = db.relationship(db.Integer, db.ForeignKey('users.id'))

    users = db.relationship('User', secondary=projects_users, back_populate='projects')
    tasks = db.relationship('Task', seconady=project_tasks, back_populate='projects')


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Intger, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(1024 * 1024))

    users = db.relationship('User', secondary=projects_users, back_populate='tasks')
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Intger, primary_key=True)
    comments = db.relationship('Comment')
    projects = db.relationship('Project', secondary=projects_users, back_populate='users')
    tasks = db.relationship('Task', secondary=projects_users, back_populate='users')


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Intger, primary_key=True)
    text = db.Column(db.String(1024 * 1024))

    user_id = db.Column(db.Intger, db.ForeignKey('users.id'))

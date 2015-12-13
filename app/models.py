from sqlalchemy import Column
from sqlalchemy import Integer, Table
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



projects_users = Table('projects_users', Base.metadata,
                               Column('project_id', Integer, ForeignKey('projects.id')),
                               Column('user_id', Integer, ForeignKey('users.id'))
                               )

users_tasks = Table('users_tasks', Base.metadata,
                            Column('task_id', Integer, ForeignKey('tasks.id')),
                            Column('user_id', Integer, ForeignKey('users.id'))
                            )

project_tasks = Table('project_tasks', Base.metadata,
                              Column('project_id', Integer, ForeignKey('projects.id')),
                              Column('task_id', Integer, ForeignKey('tasks.id'))
                              )

task_comments = Table('task_comments', Base.metadata,
                              Column('comment_id', Integer, ForeignKey('comments.id')),
                              Column('task_id', Integer, ForeignKey('tasks.id'))
                              )


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    description = Column(String(1024))
    owner_id = relationship(Integer, ForeignKey('users.id'))

    users = relationship('User', secondary=projects_users, back_populates='projects')
    tasks = relationship('Task', secondary=project_tasks, back_populates='projects')


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    description = Column(String(1024 * 1024))

    users = relationship('User', secondary=projects_users, back_populates='tasks')
    project_id = Column(Integer, ForeignKey('projects.id'))
    comments = relationship('Comment', secondary=task_comments, back_populates='tasks')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    comments = relationship('Comment')
    projects = relationship('Project', secondary=projects_users, back_populates='users')
    tasks = relationship('Task', secondary=projects_users, back_populates='users')


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    text = Column(String(1024 * 1024))

    task_id = Column(Integer, ForeignKey('tasks.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

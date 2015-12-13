from flask import Flask
from flask.ext.socketio import SocketIO
from config import config
from flask_restful import Api
from flask.ext.sqlalchemy import SQLAlchemy

socketio = SocketIO()
db = SQLAlchemy()
api = Api()


def create_app(config_name):
    """Create an application."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    api.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # api.init_app(app)
    socketio.init_app(app)

    return app

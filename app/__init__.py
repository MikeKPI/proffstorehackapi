from flask import Flask
from flask.ext.socketio import SocketIO
from config import config

socketio = SocketIO()


def create_app(config_name):
    """Create an application."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app

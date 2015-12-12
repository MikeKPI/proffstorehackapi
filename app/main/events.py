from flask import session
from flask.ext.socketio import emit, join_room, leave_room
from app import socketio


@socketio.on('connect')
def ws_connect():
    emit('status', 'seccess')

@socketio.on('join')
def ws_join(message):
    try:
        room = session.get('room')
        emit('status', 'seccess')
    except Exception:
        pass

@socketio.on('new message')
def ws_new_message(message):
    room = session.get('room')
    try:
        emit('message',
             {'usr': session.get('user'), 'msg': message},
             room=room)
    except Exception:
        pass

@socketio.on('disconnect')
def ws_disconnect():
    try:
        emit('message',
             {'usr': session.get('user'), 'msg': 'Покинул комнату'},
             room=room)
    except Exception:
        pass

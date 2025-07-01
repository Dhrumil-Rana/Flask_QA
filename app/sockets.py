from flask_socketio import SocketIO, send, emit, join_room
from .models import Message
from . import socketio, db

@socketio.on("joined")
def handle_event_joined(data):
    newRoom = data['userid'] + ":" + data['friendID']
    join_room(newRoom)

@socketio.on("sendMessage")
def handle_sendMessage_event(data):
    messageSEND = Message(msg=data['message'], senderID=data['userid'], receiverID=data['friendID'])
    db.session.add(messageSEND)
    db.session.commit()

    sendToRoom = data['friendID'] + ":" + data['userid']
    socketio.emit('receiveMessage', data, room=sendToRoom)
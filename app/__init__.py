from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from config import Config


db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object(Config)
    db.init_app(app)
    # Ensure the database is created
    with app.app_context():
        db.create_all()  # Ensure tables are created
    socketio.init_app(app, cors_allowed_origins="*") 
    from app.routes import app as main_blueprint
    app.register_blueprint(main_blueprint)
    # If you have a sockets blueprint, register it here if needed
    # from app.sockets import socketio as socketio_blueprints
    # app.register_blueprint(socketio_blueprint)
    return app
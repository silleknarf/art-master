from app import socketio, app
from config import Config

if __name__ == "__main__":
    socketio.run(app, host=Config.HOST, port=5001, debug=Config.DEBUG)

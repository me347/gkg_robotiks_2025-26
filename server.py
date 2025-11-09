from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # allow cross-origin requests

# HTTP endpoint for frontend buttons
@app.route('/command', methods=['POST'])
def command():
    data = request.get_json()
    cmd = data.get("action")  # "on" or "off"

    # Broadcast command to all connected SocketIO clients (ESP32)
    socketio.emit("command", {"action": cmd})
    return {"status": "ok", "command": cmd}

@socketio.on("connect")
def handle_connect():
    print("Client connected")

@socketio.on("disconnect")
def handle_disconnect

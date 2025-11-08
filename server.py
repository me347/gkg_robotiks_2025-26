from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os

# ===== Flask setup =====
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests
socketio = SocketIO(app, cors_allowed_origins="*")  # WebSocket support

# ===== In-memory command store =====
command = None

# ===== HTTP endpoints =====
@app.route('/command', methods=['POST'])
def set_command():
    """
    Receive command from frontend (POST request) and broadcast
    to all connected WebSocket clients (ESP32, other frontends)
    """
    global command
    data = request.get_json()
    command = data.get("action")  # expected "on" or "off"

    # Emit to all WebSocket clients instantly
    socketio.emit("command_update", {"command": command})
    return jsonify({"status": "ok", "command": command})

@app.route('/command', methods=['GET'])
def get_command():
    """
    Optional: let clients poll for the current command
    """
    return jsonify({"command": command})

# ===== Main =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    # Run with Eventlet for low-latency WebSockets
    # Install eventlet in requirements.txt: flask, flask-cors, flask-socketio, eventlet
    import eventlet
    socketio.run(app, host="0.0.0.0", port=port)

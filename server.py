from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")  # allow cross-origin

# Keep track of ESP32 clients
clients = set()

# ===== WEBSOCKET =====
@socketio.on('connect')
def handle_connect():
    clients.add(request.sid)
    print(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    clients.discard(request.sid)
    print(f"Client disconnected: {request.sid}")

# Handle custom messages from clients (optional)
@socketio.on('message')
def handle_message(msg):
    print("Received from client:", msg)

# ===== HTTP POST endpoint for frontend buttons =====
@app.route('/command', methods=['POST'])
def command():
    data = request.get_json()
    cmd = data.get("action")  # "on" or "off"

    # Broadcast to all connected ESP32 clients
    socketio.emit('message', cmd)
    print(f"Broadcasting command: {cmd}")

    return jsonify({"status": "ok", "command": cmd})

# ===== RUN SERVER =====
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port, ssl_context="adhoc")  # WSS

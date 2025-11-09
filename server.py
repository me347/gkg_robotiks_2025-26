from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow cross-origin requests

# ===== HTTP POST endpoint for frontend buttons =====
@app.route('/command', methods=['POST'])
def command():
    data = request.get_json()
    cmd = data.get("action")  # "on" or "off"
    
    # Broadcast command to all connected clients (ESP32)
    socketio.emit("command", {"action": cmd})
    print(f"Broadcasting command: {cmd}")
    return {"status": "ok", "command": cmd}

# ===== SocketIO events =====
@socketio.on("connect")
def handle_connect():
    print("Client connected")

@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")

# ===== Run server =====
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)

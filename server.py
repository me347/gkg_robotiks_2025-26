import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow requests from any origin

# Store the latest command
command = None

@app.route('/command', methods=['POST'])
def set_command():
    """Receive a command from the website (e.g., 'on' or 'off')"""
    global command
    data = request.get_json()
    if not data or 'action' not in data:
        return jsonify({'status': 'error', 'message': 'No action provided'}), 400
    command = data['action']
    return jsonify({'status': 'ok', 'command': command})

@app.route('/command', methods=['GET'])
def get_command():
    """Return the latest command for the ESP32 to read"""
    return jsonify({'command': command})

@app.route('/')
def index():
    return "ESP32 backend is running!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

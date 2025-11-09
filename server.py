# server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import websockets
import threading

app = Flask(__name__)
CORS(app)

# ------------------------------
# Your existing backend logic
# ------------------------------
button_state = False  # Example shared state

@app.route("/button", methods=["POST"])
def set_button():
    global button_state
    data = request.json
    button_state = bool(data.get("state", False))
    return jsonify({"status": "ok", "state": button_state})

@app.route("/button", methods=["GET"])
def get_button():
    return jsonify({"state": button_state})

# ------------------------------
# Raw WebSocket server for ESP32
# ------------------------------
clients = set()

async def esp_ws_handler(websocket, path):
    clients.add(websocket)
    try:
        while True:
            await websocket.send(str(button_state))
            await asyncio.sleep(0.05)  # 50ms update
    except websockets.ConnectionClosed:
        pass
    finally:
        clients.remove(websocket)

def start_ws_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ws_server = websockets.serve(esp_ws_handler, "0.0.0.0", 8765)
    loop.run_until_complete(ws_server)
    loop.run_forever()

# ------------------------------
# Start Flask + WebSocket server
# ------------------------------
if __name__ == "__main__":
    # Run WebSocket server in a separate thread
    ws_thread = threading.Thread(target=start_ws_server)
    ws_thread.start()

    # Run Flask server
    app.run(host="0.0.0.0", port=5000)

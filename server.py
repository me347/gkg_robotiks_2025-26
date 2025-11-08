from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sockets import Sockets

app = Flask(__name__)
CORS(app)
sockets = Sockets(app)

clients = []

@sockets.route('/ws')
def ws_route(ws):
    clients.append(ws)
    print("Client connected")
    try:
        while not ws.closed:
            msg = ws.receive()
            if msg:
                print("Received:", msg)
    finally:
        clients.remove(ws)
        print("Client disconnected")

@app.route('/command', methods=['POST'])
def command():
    data = request.get_json()
    cmd = data.get("action", "")
    print("Command from frontend:", cmd)

    for ws in list(clients):
        try:
            ws.send(cmd)
        except:
            clients.remove(ws)

    return jsonify({"status": "ok", "command": cmd})

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    port = 5000
    print(f"Server running on http://0.0.0.0:{port}")
    server = pywsgi.WSGIServer(("0.0.0.0", port), app, handler_class=WebSocketHandler)
    server.serve_forever()

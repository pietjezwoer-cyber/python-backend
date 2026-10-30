from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "https://python-backend-y3ul.onrender.com"])

devices = []
frames = {}  # device name -> base64 jpeg

@app.route('/')
def home():
    return "backend running"

@app.route('/api/devices', methods=['GET'])
def list_devices():
    return jsonify(devices)

@app.route('/api/devices', methods=['POST'])
def add_device():
    devices.append(request.json)
    return jsonify({"ok": True})

@app.route('/api/command', methods=['POST'])
def command():
    return jsonify({"ok": True, "output": "command received"})

@app.route('/api/frame', methods=['POST'])
def upload_frame():
    data = request.json
    device = data.get('device')
    image = data.get('image')
    if device and image:
        frames[device] = image
    return jsonify({"ok": True})

@app.route('/api/frame', methods=['GET'])
def get_frame():
    device = request.args.get('device')
    img = frames.get(device)
    if img:
        return jsonify({"image": img})
    return jsonify({"image": None})

@app.route('/api/stream/<device>', methods=['GET'])
def stream(device):
    img = frames.get(device)
    if img:
        return jsonify({"image": img})
    return jsonify({"image": None})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
```

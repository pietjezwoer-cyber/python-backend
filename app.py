from flask import Flask, request, jsonify

app = Flask(__name__)
devices = []

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
    return jsonify({"ok": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
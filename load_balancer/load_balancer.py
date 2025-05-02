
from flask import Flask, request
import requests
import threading
import time
import itertools

app = Flask(__name__)

server_list = [
    "http://server1:5000",
    "http://server2:5000",
    "http://server3:5000"
]

healthy_servers = []
lock = threading.Lock()
server_cycle = None

def health_check():
    global healthy_servers, server_cycle
    while True:
        alive = []
        for server in server_list:
            try:
                r = requests.get(server + "/heartbeat", timeout=1)
                if r.status_code == 200:
                    alive.append(server)
            except:
                continue
        with lock:
            healthy_servers = alive
            server_cycle = itertools.cycle(healthy_servers) if healthy_servers else None
        time.sleep(3)  # Check every 3 seconds

def get_next_server():
    with lock:
        if server_cycle:
            return next(server_cycle)
        else:
            return None

@app.route('/upload', methods=['POST'])
def upload():
    server = get_next_server()
    if server:
        files = {'file': request.files['file']}
        r = requests.post(server + '/upload', files=files)
        return r.text, r.status_code
    else:
        return "No available servers", 503

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    server = get_next_server()
    if server:
        r = requests.get(server + f'/download/{filename}')
        return (r.content, r.status_code, {'Content-Type': r.headers['Content-Type']})
    else:
        return "No available servers", 503

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return 'Load Balancer Alive', 200

if __name__ == '__main__':
    threading.Thread(target=health_check, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)

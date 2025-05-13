from flask import Flask, request, redirect
import requests
import threading
import time
import itertools
import logging
from urllib.parse import urljoin

app = Flask(__name__)

# Configuration
AUTH_SERVER = "http://localhost:8081"
FILE_SERVERS = [
    "http://server1:5000",
    "http://server2:5000",
    "http://server3:5000"
]

# Health check setup (same as before)
healthy_servers = []
lock = threading.Lock()
server_cycle = None
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def health_check():
    global healthy_servers, server_cycle
    while True:
        alive = []
        for server in FILE_SERVERS:
            try:
                r = requests.get(urljoin(server, "/heartbeat"), timeout=1)
                if r.status_code == 200:
                    alive.append(server)
            except:
                logger.warning(f"Server {server} is down")
                continue
        
        with lock:
            healthy_servers = alive
            server_cycle = itertools.cycle(healthy_servers) if healthy_servers else None
            if healthy_servers:
                logger.info(f"Healthy servers: {healthy_servers}")
        time.sleep(3)

def get_next_server():
    with lock:
        return next(server_cycle) if server_cycle else None

# Authentication routes -> Client
@app.route('/')
def index():
    return redirect(AUTH_SERVER)

@app.route('/login')
def login():
    return redirect(urljoin(AUTH_SERVER, "/login"))

@app.route('/signup')
def signup():
    return redirect(urljoin(AUTH_SERVER, "/signup"))

# File operations -> Backend servers
@app.route('/upload', methods=['POST'])
def upload():
    if not request.cookies.get('session'):
        return redirect(urljoin(AUTH_SERVER, "/login"))
    
    server = get_next_server()
    if server:
        try:
            files = {'file': request.files['file']}
            r = requests.post(urljoin(server, '/upload'), files=files, cookies=request.cookies)
            return r.text, r.status_code
        except Exception as e:
            logger.error(f"Upload error: {e}")
            return "Upload failed", 500
    return "No available servers", 503

@app.route('/download/<filename>')
def download(filename):
    if not request.cookies.get('session'):
        return redirect(urljoin(AUTH_SERVER, "/login"))
    
    server = get_next_server()
    if server:
        try:
            r = requests.get(urljoin(server, f'/download/{filename}'), cookies=request.cookies)
            return (r.content, r.status_code, dict(r.headers))
        except Exception as e:
            logger.error(f"Download error: {e}")
            return "Download failed", 500
    return "No available servers", 503

@app.route('/heartbeat')
def heartbeat():
    return 'Load Balancer Alive', 200

if __name__ == '__main__':
    threading.Thread(target=health_check, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
from flask import Flask, request, send_from_directory
import os
import socket  # To identify the server hostname
import logging

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Set up logging to file and console
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    # Log which server handled the upload request
    hostname = socket.gethostname()
    app.logger.info(f"[{hostname}] Handled upload: {file.filename}")

    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return f'File uploaded successfully by {hostname}', 200

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # Log which server is serving the download
    hostname = socket.gethostname()
    app.logger.info(f"[{hostname}] Handling download for: {filename}")
    
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    app.logger.info("Heartbeat check")
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

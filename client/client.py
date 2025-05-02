from flask import Flask, request, send_from_directory, render_template
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/app/uploads'

# Ensure directory exists with proper permissions
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.chmod(UPLOAD_FOLDER, 0o777)  # Make sure it's writable

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    return f"File {file.filename} uploaded successfully."

@app.route('/download')
def download():
    filename = request.args.get('filename')
    if not filename:
        return "Filename is required", 400
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(filepath):
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    return f"File {filename} not found.", 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
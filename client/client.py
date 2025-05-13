from flask import Flask, request, send_from_directory, render_template, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
from functools import wraps

app = Flask(__name__,
            static_folder='auth',    # Serve static files from /auth
            template_folder='auth')  # Look for templates in /authUPLOAD_FOLDER = '/app/uploads'
app.secret_key = 'kgrgjkoOO0848HFJIDJCIo'  
UPLOAD_FOLDER = '/app/uploads'

# Auth setup
USERS_FILE = os.path.join(os.path.dirname(__file__), 'users.json')

def load_users():
    try:
        with open(USERS_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {'users': []}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Auth routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        users = load_users()
        
        user = next((u for u in users['users'] if u['email'] == email), None)
        if user and check_password_hash(user['password_hash'], password):
            session['user'] = email
            return redirect(url_for('index'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        users = load_users()
        
        if any(u['email'] == email for u in users['users']):
            flash('Email already exists')
            return redirect(url_for('signup'))
        
        users['users'].append({
            'email': email,
            'password_hash': generate_password_hash(password)
        })
        save_users(users)
        flash('Account created! Please login.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# Your existing routes (protected with login_required)
@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
@login_required
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
@login_required
def download():
    filename = request.args.get('filename')
    if not filename:
        return "Filename is required", 400
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(filepath):
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    return f"File {filename} not found.", 404

# Initialize upload folder
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.chmod(UPLOAD_FOLDER, 0o777)  # Make sure it's writable

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
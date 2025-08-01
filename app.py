import os
import json
from flask import Flask, render_template, request, redirect, url_for, session, flash
import config

app = Flask(__name__)

# --- Configuration ---
app.secret_key = config.FLASK_SECRET_KEY
APP_PASSWORD = config.APP_PASSWORD

SETTINGS_FILE = 'settings.json'
LOG_FILE = 'log.txt'

# --- Helper Functions ---

def read_settings():
    """Reads settings from the JSON file."""
    if not os.path.exists(SETTINGS_FILE):
        # Default settings if the file doesn't exist
        return {
            "recipient_email": "susan.jetlearn@gmail.com",
            "subject": "Monthly Reminder",
            "body": "Hi Dad, don’t forget to pay your employees today 😊",
            "send_day": 25 # Default day
        }
    with open(SETTINGS_FILE, 'r') as f:
        # Load existing settings and ensure send_day has a default
        settings = json.load(f)
        if 'send_day' not in settings:
            settings['send_day'] = 25
        return settings

def write_settings(settings):
    """Writes settings to the JSON file."""
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

def read_logs():
    """Reads log entries, returning the most recent first."""
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, 'r') as f:
        return f.readlines()[::-1]

# --- Web Routes ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles the login page."""
    if request.method == 'POST':
        if request.form.get('password') == APP_PASSWORD:
            session['logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Incorrect password.', 'danger')
    return render_template('login.html')

@app.route('/')
def index():
    """Main page to show settings and logs."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    settings = read_settings()
    logs = read_logs()
    return render_template('index.html', settings=settings, logs=logs)

@app.route('/save', methods=['POST'])
def save_settings():
    """Saves the updated settings from the form."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    new_settings = {
        # IMPORTANT: Convert the day to an integer
        "send_day": int(request.form.get('send_day')),
        "recipient_email": request.form.get('recipient_email'),
        "subject": request.form.get('subject'),
        "body": request.form.get('body')
    }
    write_settings(new_settings)
    flash('Settings saved successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
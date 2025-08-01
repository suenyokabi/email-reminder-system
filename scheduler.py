import os
import datetime
import base64
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText

# --- Configuration ---
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
SETTINGS_FILE = 'settings.json'
LOG_FILE = 'log.txt'
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

def log_message(message):
    """Appends a timestamped message to the log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a') as f:
        f.write(f"{timestamp} - {message}\n")
    print(message)

def read_settings():
    """Reads settings from the JSON file."""
    try:
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        log_message(f"ERROR: {SETTINGS_FILE} not found. Cannot send email.")
        return None

def is_send_day(settings):
    """Checks if today is the configured send day."""
    # Get the day from settings, defaulting to 25 if not found.
    target_day = settings.get('send_day', 25)
    return datetime.date.today().day == target_day

# --- Gmail functions (gmail_authenticate and send_email) remain unchanged ---

def gmail_authenticate():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def send_email(service, settings):
    try:
        recipient = settings['recipient_email']
        subject = settings['subject']
        body = settings['body']
        message = MIMEText(body)
        message['to'] = recipient
        message['subject'] = subject
        create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
        send_message = (service.users().messages().send(userId="me", body=create_message).execute())
        log_message(f"SUCCESS: Email sent to {recipient}. Message ID: {send_message['id']}")
    except Exception as e:
        log_message(f"ERROR: Failed to send email. Details: {e}")


def main():
    """Main function to run the scheduled task."""
    settings = read_settings()
    
    if settings:
        # Pass the settings to the date-checking function
        if is_send_day(settings):
            log_message(f"Task starting: Today is the configured send day ({settings['send_day']}).")
            service = gmail_authenticate()
            send_email(service, settings)
        else:
            print(f"Task starting: Not the configured send day. No action needed.")
    else:
        # This will be printed if settings.json is missing
        print("Task starting: Settings file not found. No action taken.")

if __name__ == '__main__':
    main()
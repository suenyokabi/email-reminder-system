Automated Monthly Email Reminder
This is a simple yet powerful Python application that sends an automated reminder email on a configurable day of the month. It features a secure backend using the Google Gmail API (via OAuth 2.0) and a user-friendly web interface built with Flask for easy configuration.
The entire system is designed to be hosted for free on platforms like PythonAnywhere.
✨ Features
Automated Emailing: Uses a scheduled script to send emails automatically.
Web Interface: A simple, password-protected web UI to configure settings without touching the code.
Fully Configurable: Easily change the recipient's email, the subject, the email body, and the day of the month for the reminder.
Send Log Viewer: The web UI displays a log of when emails were successfully sent.
Secure: Uses the official Google Gmail API with OAuth 2.0, so your password is never stored or used. Secrets are managed securely outside of the main codebase.
Free Hosting: Designed to run on the free tiers of services like PythonAnywhere.
📸 Screenshot
Here's a look at the web interface where you can manage all your settings.
(Note: To create this screenshot, run the app locally, log in, and take a picture of the settings page. Save it as screenshot.png in your project folder.)
![alt text](screenshot.png)
🛠️ Technology Stack
Backend: Python 3
Web Framework: Flask
Email API: Google Gmail API (via google-api-python-client)
Scheduling: Cron job or Scheduled Task (on the hosting platform)
🚀 Setup and Installation
Follow these steps to get the project running on your local machine.
1. Clone the Repository
Generated bash
git clone https://github.com/suenyokabi2020/EMAIL REMINDER SYSTEM.git
cd your-repo-name```




3. Install Dependencies
Install all the required Python libraries from the requirements.txt file.
Generated bash
pip install -r requirements.txt
Use code with caution.
Bash
4. Set Up the Google Gmail API
This is the most important setup step. You need to authorize your application to send emails on your behalf.
Follow the official Google instructions to enable the Gmail API for your project.
During the setup, when asked to Create Credentials, choose "OAuth client ID".
For the "Application type", you must select "Desktop app".
After creating the client ID, a "DOWNLOAD JSON" button will appear. Click it to download your credentials.
Crucial: Rename the downloaded file to exactly credentials.json and place it in the root directory of this project.
⚙️ Configuration
This project keeps all secrets out of the main codebase for security. You must create a config.py file.
This file is listed in .gitignore and will NOT be committed to GitHub.
In the root of the project folder, create a new file named config.py.
Copy the following code into your config.py and fill in your secrets.
Generated python
# config.py - This file contains your secret keys.
# It is ignored by Git and will NOT be uploaded to GitHub.

# To generate a strong, random secret key, run this command in your terminal:
# python -c 'import secrets; print(secrets.token_hex(16))'
FLASK_SECRET_KEY = "your-super-long-random-secret-key-here"

# This is the password you will use to log in to the web interface.
APP_PASSWORD = "your-secure-web-login-password-here"
Use code with caution.
Python
▶️ Running the Application Locally
You must run the scheduler.py script once first to generate your token.json.
Step 1: First-Time Authentication (Crucial)
This step authorizes the application with your Google account and creates the token.json file.
Run the scheduler script from your terminal:
Generated bash
python scheduler.py
Use code with caution.
Bash
Your web browser will open automatically.
Log in to the Google account you used to enable the API.
You may see a warning screen saying "Google hasn't verified this app". Click "Advanced" and then "Go to [Your App Name] (unsafe)". This is expected for personal projects.
Grant the application permission to send emails.
Once you allow it, the script will finish, and a token.json file will appear in your project folder.
Step 2: Run the Web App
Now you can start the Flask web server.
Generated bash
python app.py
Use code with caution.
Bash
Your web interface is now running! Open your browser and go to http://127.0.0.1:5001/. Log in with the APP_PASSWORD you set in config.py and configure your reminder.
☁️ Deployment
This application is designed to be deployed to PythonAnywhere.
Upload Files: Upload all project files (.py, .html, requirements.txt, credentials.json, token.json) to a new folder on PythonAnywhere.
Create config.py: Manually create the config.py file on the server and paste in your secrets.
Web App: Set up a new Flask "Web App" on the Web tab, pointing it to your project folder and WSGI file.
Scheduled Task: Set up a "Scheduled Task" on the Tasks tab to run the scheduler.py script once a day. The command should be: python3.xx /home/YourUsername/your-project-folder/scheduler.py (use your specific Python version and paths).
Re-authenticate: You may need to run the scheduler.py script once from a Bash console on PythonAnywhere to generate a server-specific token.json.
📈 Future Improvements
Send notifications to other platforms like Telegram or Discord.
Upgrade the logging system to store logs in a database or a Google Sheet.
Add a "Send Test Email" button to the web UI.
from flask import Flask, render_template, request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from urllib.parse import quote as url_quote  # Use urllib.parse for compatibility

# Load environment variables from the .env file
load_dotenv()

# Define Flask app
app = Flask(__name__)

# Fetch email configurations from environment variables
MAIL = os.getenv('MAIL')
RECEIVER = os.getenv('RECEIVER')
PASSWORD = os.getenv('PASSWORD')
SUBJECT = "Guest Feedback"

@app.route("/")
def home():
    """Render the home page."""
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    """Handle contact form submissions."""
    if request.method == "POST":
        # Grab the data from the form
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        # Send the email
        success = send_email(name, email, subject, message)

        if success:
            return render_template("thank_you.html")  # Success page
        else:
            return render_template("error.html")  # Error page

def send_email(name, email, subject, message):
    """Send an email using SMTP."""
    try:
        # Set up the SMTP server
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Compose the email
        msg = MIMEMultipart()
        msg['From'] = MAIL
        msg['To'] = RECEIVER
        msg['Subject'] = subject

        # Email body content
        body = f"""
        You have received a new message from the contact form:

        Name: {name}
        Email: {email}
        Subject: {subject}
        Message:
        {message}
        """
        msg.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(MAIL, PASSWORD)
        server.sendmail(MAIL, RECEIVER, msg.as_string())
        server.quit()

        print("Email sent successfully.")
        return True
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
        return False

if __name__ == "__main__":



    app.run(debug=True, port=5001)


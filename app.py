from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

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
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    if request.method == "POST":
        # Grab the data from the form
        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]

        # Send the email
        success = send_email(name, email, subject, message)

        if success:
            # Redirect to a thank you page or show a success message
            return render_template("thank_you.html")
        else:
            # Redirect to an error page or show an error message
            return render_template("error.html")


def send_email(name, email, subject, message):
    try:
        # Set up the SMTP server (This is for Gmail. Modify for other services)
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

        # Connect to the SMTP server and send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(MAIL, PASSWORD)
        server.sendmail(MAIL, RECEIVER, msg.as_string())
        server.quit()

        return True  # Indicating success
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
        return False  # Indicating failure


if __name__ == "__main__":
    from waitress import serve

    app.run(debug=True, port=5001)

    # serve(app, host='0.0.0.0', port=5001)

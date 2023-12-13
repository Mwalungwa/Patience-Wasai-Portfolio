from flask import Flask, render_template, request, flash
from flask_bootstrap import Bootstrap
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date
import os
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
bootstrap = Bootstrap(app)

MY_EMAIL = os.environ['EMAIL_ADDRESS']
MY_PASSWORD = os.environ['EMAIL_PASSWORD']


def send_email(name, email, message):
    # Your email credentials and server information
    sender_email = MY_EMAIL
    sender_password = MY_PASSWORD
    smtp_server = os.environ['EMAIL_SERVER']

    # Create the email message
    subject = "New message from your website"
    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = MY_EMAIL  # Replace with your email address
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        # Send the email
        server.sendmail(sender_email, MY_EMAIL, message.as_string())


@app.route('/', methods=['GET', 'POST'])
def index():  # put application's code here
    current_date = date.today()

    def is_valid_email(email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        valid = re.fullmatch(regex, email)
        if valid:
            return True
        else:
            return False

    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        #check data
        missing_fields = []
        if not name.strip():
            missing_fields.append("name")
        if not email.strip():
            missing_fields.append("email address")
        if not message.strip():
            missing_fields.append("email address")

        if missing_fields:
            flash(f"Please fill in the following fields: {', '.join(missing_fields)}")

        print(is_valid_email(email))
        if is_valid_email(email) == True:
            # Send email
            send_email(name, email, message)
            first_name = name.split(" ")[0]
            flash(
                f'Hi {first_name}, your message has been successfully sent. I will get back to you as soon as possible.')
        else:
            flash("Enter a valid email")

    return render_template('index.html', current_year = current_date.year)


if __name__ == '__main__':
    app.run(debug=True)

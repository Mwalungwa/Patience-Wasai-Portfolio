from flask import Flask, render_template, request, flash
from flask_bootstrap import Bootstrap
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

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
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Send email
        send_email(name, email, message)
        ref_name = name.split(" ")
        flash(f'Hi {ref_name[0]}, your message has been succesfully sent. I will get back to you as soon an possible.')


    return render_template('index.html', )


if __name__ == '__main__':
    app.run(debug=True)

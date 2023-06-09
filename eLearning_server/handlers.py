import random, string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import redis

def generate_code():
    return random.randint(100000, 999999)

def send_code(**kwargs):
    code = generate_code()

    msg = MIMEMultipart()
    msg['From'] = 'no-reply@mentor.md'
    msg['To'] = kwargs.get('receiver')
    msg['Subject'] = 'Password recovery'

    # Add HTML content to the message body
    html = f"""
    <html>
    <body>
        <p>Your code is - <b>{code}</b></p>
        <p>Enter this in recovery form and follow the instructions!</p>
        <span><b>It will only be active for 10 minutes!!!</b></span>
        <br><br>
        <p>Best regards, <br>Administration =)</p>
    </body>
    </html>
    """
    msg.attach(MIMEText(html, 'html'))

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login('noreply.m3nt0r@gmail.com', 'yvfskiltbgpgnaeb')
        smtp.send_message(msg)
    return code


13099

def generate_reedem_code():
    code_length = 16
    chars = string.ascii_letters + string.digits
    code = ''.join(random.choice(chars) for _ in range(code_length))
    return code

# docker run --name redis -p 6379:6379 -d redis
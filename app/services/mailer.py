import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

email_host = os.getenv("EMAIL_HOST")
email_pwd = os.getenv("EMAIL_LOGIN_PASSWORD") 

def send_email(subject, body, to_email):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = email_host
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_host, email_pwd)
            smtp.send_message(msg)
        return True
    except smtplib.SMTPException as e:
        print(f"Error enviando correo: {e}")
        return False
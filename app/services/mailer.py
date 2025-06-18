import smtplib
from email.message import EmailMessage

def send_email(subject, body, to_email, from_email, password):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.send_message(msg)
        return True
    except smtplib.SMTPException as e:
        print(f"Error enviando correo: {e}")
        return False
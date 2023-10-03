import smtplib
from config import EMAIL, EMAIL_PASSWORD, EMAIL_PORT, EMAIL_SERVER
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(to: str, subject: str, message_text: str):
    message = MIMEMultipart()

    message['FROM'] = EMAIL
    message['TO'] = to
    message["Subject"] = subject
    message.attach(MIMEText(message_text, "plain"))

    with smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(EMAIL, EMAIL_PASSWORD)
        server.sendmail(EMAIL, to, message.as_string())
        server.quit()

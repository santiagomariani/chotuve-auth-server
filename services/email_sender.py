from .html import html
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class EmailSender():
    def send_reset_password_email(self, receiver_email, code):
        html_with_code = html.format(code)
        
        message = Mail(
            from_email='chotuvevideos@gmail.com',
            to_emails=receiver_email,
            subject='Recuperar contraseña de Chotuve',
            html_content=html_with_code)
        try:
            sg = SendGridAPIClient(os.environ.get('SMTP_PASS'))
            response = sg.send(message)
        except Exception as e:
            print(e.message)

class EmailSenderFake():

    def send_reset_password_email(self, receiver_email, code):
        True


email_sender_service = EmailSender() if (os.environ['APP_SETTINGS'] != 'testing') else EmailSenderFake()

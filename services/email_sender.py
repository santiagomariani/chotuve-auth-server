import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailSender():
    # refactor this to get credentials from some safe place.
    _SENDER_EMAIL = "chotuvevideos@gmail.com"
    _PASSWORD = "Lamejorappgrupo8"

    def send_reset_password_email(self, receiver_email, code):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Recuperar contraseña de Chotuve"
        message["From"] = self._SENDER_EMAIL 
        message["To"] = receiver_email

        # plain text version
        text = """\
        Hola,
        Para recuperar tu cuenta de Chotuve toma el siguiente codigo de 6 digitos e insertalo en la aplicacion mobil.
        {}
        Si no has solicitado este cambio, ignora este correo electrónico.
        Gracias,
        El equipo de Chotuve Videos.
        """.format(code)

        # html version
        html = """\
        <html>
        <body>
            <p>Hola:</p>
            <p>Para recuperar tu cuenta de Chotuve toma el siguiente codigo de 6 digitos e insertalo en la aplicacion mobil.</p>
            <p><b>{}</b></p>
            <p>Si no has solicitado este cambio, ignora este correo electrónico.</p>
            <p>Gracias,</p>
            <p>El equipo de Chotuve.</p>
        </body>
        </html>
        """.format(code)

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self._SENDER_EMAIL, self._PASSWORD)
            server.sendmail(
                self._SENDER_EMAIL, receiver_email, message.as_string()
            )

class EmailSenderFake():

    def send_reset_password_email(self, receiver_email, code):
        True

email_sender_service = EmailSender() if os.environ['APP_SETTINGS'] != 'testing' else EmailSenderFake()

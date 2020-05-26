import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender():

    def __init__(self, receiver_email):
        self.receiver_email = receiver_email
        self.sender_email = "chotuvevideos@gmail.com"
        self.password = "Lamejorappgrupo8"

    def send_reset_password_email(self, code):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Recuperar contraseña de Chotuve"
        message["From"] = self.sender_email
        message["To"] = self.receiver_email

        # plain text version
        text = """\
        Hola,
        Para recuperar tu cuenta de Chotuve toma el siguiente codigo de 6 digitos e insertalo en la aplicacion mobil.
        {}
        Si no has solicitado este cambio, ignora este correo electrónico.
        Gracias,
        El equipo de Chotuve.
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
            server.login(self.sender_email, self.password)
            server.sendmail(
                self.sender_email, self.receiver_email, message.as_string()
            )
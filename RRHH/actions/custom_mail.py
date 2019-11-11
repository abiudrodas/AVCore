import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pickle
import base64

def send_email(user, user_mail, subject, additional_data=[None]):
    # The mail addresses and password
    with open('mail.pickle', 'rb') as handle:
        mail = pickle.load(handle)

    mail_content = '''Hola {}, Te informamos que el usuario {} está solicitando vacaciones para el periodo {}, 
    para aprobar esta solicitud accede al siguiente enlace {}
    Saludos \n RRHH bot'''.format("i.fernandez", user, additional_data[0], "[link to CRM]")
    sender_address = base64.b64decode(mail['user']).decode("utf-8")
    sender_pass = base64.b64decode(mail['pass']).decode("utf-8")
    receiver_address = user_mail
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subject  # The subject line
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')


if __name__ == "__main__":
    user = "a.rojas"
    subject = "Peticion de vacaciones"
    user_email = "abiudrodas@holahal.com"
    periodo = ["20-11-19 al 03-01-20"]
    send_email(user=user, user_mail=user_email, subject=subject, additional_data=periodo)

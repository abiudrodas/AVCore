from fpdf import FPDF
from twilio.rest import Client
import os

def generate_nomina(month):
    # class object FPDF() which is predefiend in side the package fpdf.
    document = FPDF()
    document.add_page()
    # font size setting of the page
    document.set_font("Arial", size=15)
    # txt message will displayed on pdf page  at the center.
    document.cell(200, 10, txt="Simulación Nomina del " + month, ln=1, align="L")

    document.image("nomina.jpg", w=150, h=200)
    # pdf file naming.
    name = "nomina_" + month + ".pdf"
    document.output(name)
    # creating page format A4 Or A3 Or ...
    document = FPDF(orientation='P', unit='mm', format='A4')
    link = upload_file_exp(name)
    os.remove(name)

    send_whatsapp(msg="Aqui tienes la nomina del "+month, phone_to='whatsapp:+34634146030', attachment=link)


def send_whatsapp(msg, phone_to=None, attachment=None):
    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    account_sid = "ACe87a63fe61178c294fd915c1ab1a5db5"
    auth_token = "e4e45fb2cd61f29a4973e68b922557b4"
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        from_='whatsapp:+14155238886',
        body=msg,
        to=phone_to,
        media_url=attachment
    )

def upload_file_exp(name=None):
    import requests

    url = "https://file.io"

    with open(name, 'rb') as f:
        res = requests.post(url, files={'file': f})

    return res.json()['link']


if __name__ == "__main__":
    nomina = "08-2019"
    generate_nomina(nomina)





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

    return link


def upload_file_exp(name=None):
    import requests

    url = "https://file.io"

    with open(name, 'rb') as f:
        res = requests.post(url, files={'file': f})

    return res.json()['link']


if __name__ == "__main__":
    nomina = "08-2019"
    generate_nomina(nomina)





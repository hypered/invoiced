from invoice2data import extract_data
from invoice2data.extract.loader import read_templates
from PIL import Image
from pyzbar.pyzbar import decode
from segno import helpers

def extract_data_from_pdf(pdf_path):
    templates = read_templates('./templates/')
    result = extract_data(pdf_path, templates=templates)
    print(result)

def generate_qr_code_from_pdf(pdf_path):
    templates = read_templates('./templates/')
    result = extract_data(pdf_path, templates=templates)
    if result.get('paid', False):
        print('Invoice is marked as paid.')
    else:
        qrcode = helpers.make_epc_qr(name=result['issuer'],
                                     iban=result['iban'],
                                     bic=result['bic'],
                                     amount=result['amount'],
                                     reference=result['reference'])
        qrcode.save('qrcode.png', scale=8)
        print('QR code generated as qrcode.png.')

def display_qr_code_content(file_path):
    img = Image.open(file_path)
    decoded_data = decode(img)

    if decoded_data:
        s = decoded_data[0].data.decode("utf-8")
        print("QR Code content:")
        print(s)
        return s
    else:
        print("No QR code found in the image.")
        return None

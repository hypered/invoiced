from invoice2data import extract_data
from invoice2data.extract.loader import read_templates
from PIL import Image
from pyzbar.pyzbar import decode

def extract_data_from_pdf(pdf_path):
    templates = read_templates('./templates/')
    result = extract_data(pdf_path, templates=templates)
    print(result)

def generate_qr_code_from_pdf(pdf_path):
    print("TODO")

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

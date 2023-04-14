import binascii
from invoice2data import extract_data
from invoice2data.extract.loader import read_templates
from jinja2 import Environment, FileSystemLoader
import mmh3
import os
from PIL import Image
from pyzbar.pyzbar import decode
from segno import helpers
import subprocess

TEMPLATES = None
def load_templates():
    global TEMPLATES
    if TEMPLATES is None:
        TEMPLATES = read_templates('./templates/')
    return TEMPLATES

def extract_data_from_pdf(pdf_path):
    templates = load_templates()
    result = extract_data(pdf_path, templates=templates)
    return result

def generate_qr_code_from_pdf(pdf_path, out_directory):
    result = extract_data_from_pdf(pdf_path)
    generate_qr_code_from_data(result, out_directory)

def generate_qr_code_from_data(result, out_directory):
    if result.get('paid', False):
        print('Invoice is marked as paid.')
    else:
        os.makedirs(out_directory, exist_ok=True)
        output_path = os.path.join(out_directory, 'qrcode.png')
        qrcode = helpers.make_epc_qr(name=result['issuer'],
                                     iban=result['iban'],
                                     bic=result['bic'],
                                     amount=result['amount'],
                                     reference=result['reference'])
        qrcode.save(output_path, scale=8)
        print(f'QR code generated at {output_path}.')

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

def convert_pdf_to_png(pdf_path, out_directory):
    """
    Convert the first page of a PDF to a PNG.
    This is equivalent to
        convert -quality 100 -density 200 -colorspace sRGB "some.pdf[0]" \
            -flatten output.png
    """
    os.makedirs(out_directory, exist_ok=True)
    output_path = os.path.join(out_directory, 'output.png')
    args = [
        "convert",
        "-quality", "100",
        "-density", "200",
        "-colorspace", "sRGB",
        f"{pdf_path}[0]",
        "-flatten",
        output_path,
        ]
    proc = subprocess.run(
            args,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True,
        )
    output = proc.stdout
    print(f'Image generated as {output_path}.')

def generate_hash_from_invoice(pdf_path):
    seed = 0
    with open(pdf_path, 'rb') as f:
        file_data = f.read()
    byte_data = mmh3.hash_bytes(file_data, seed)
    return binascii.hexlify(byte_data).decode('utf-8')

def process_pdf(pdf_path, out_directory):
    result = extract_data_from_pdf(pdf_path)
    generate_qr_code_from_data(result, out_directory)
    convert_pdf_to_png(pdf_path, out_directory)
    return result

def generate_html_from_invoice(pdf_path, out_directory):
    result = process_pdf(pdf_path, out_directory)

    template_path = 'jinja2/preview.html'
    template_dir, template_file = os.path.split(template_path)
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_file)

    content = {
        "image_url": 'output.png',
        "qr_code_url": 'qrcode.png',
        "iban": result['iban'],
        "amount": result['amount'],
        "reference": result['reference'],
    }

    rendered_template = template.render(content)

    os.makedirs(out_directory, exist_ok=True)
    output_path = os.path.join(out_directory, 'output.html')
    with open(output_path, "w") as output_file:
        output_file.write(rendered_template)
    print(f'HTML page generated at {output_path}.')

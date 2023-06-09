import binascii
import datetime
import fnmatch
from invoice2data import extract_data
from invoice2data.extract.loader import read_templates
from jinja2 import Environment, FileSystemLoader
import mmh3
import os
from PIL import Image
from pyzbar.pyzbar import decode
from segno import helpers
import subprocess
import sys

from . import db

JINJA2_TEMPLATES_DIR = os.environ.get('JINJA2_TEMPLATES_DIR',
    os.path.abspath('./jinja2/'))
YAML_TEMPLATES_DIR = os.environ.get('YAML_TEMPLATES_DIR', './templates/')

YAML_TEMPLATES = None
def load_invoice2data_templates():
    global YAML_TEMPLATES
    if YAML_TEMPLATES is None:
        YAML_TEMPLATES = read_templates(YAML_TEMPLATES_DIR)
    return YAML_TEMPLATES

def extract_data_from_pdf(pdf_path):
    templates = load_invoice2data_templates()
    result = extract_data(pdf_path, templates=templates)
    if result:
        validate_data(result)
    return result

class ExtractException(Exception):
    def __init__(self, message):
        super().__init__(message)

def validate_data(result):
    def check(field_name, field_type):
        if field_name not in result:
            raise ExtractException(f"The field '{field_name}' is missing.")
        if type(result[field_name]) != field_type:
            raise ExtractException(f"The field '{field_name}' is not a {field_type.__name__}.")
    for field_name, field_type in [
        ('issuer', str),
        ('date', datetime.datetime),
        ('amount', float), # TODO Decimal
        ('invoice_number', str),
        ]:
        check(field_name, field_type)

    # Payment information can fail to be extracted.
    if 'iban' in result:
        check('iban', str)
    if 'bic' in result:
        check('bic', str)
    if 'reference' in result:
        check('reference', str)
        if 'text' in result:
            raise ExtractException(f"Both fields 'text' and 'reference' are present.")
    if 'text' in result:
        check('text', str)
        if 'reference' in result:
            raise ExtractException(f"Both fields 'text' and 'reference' are present.")

def make_qrcode_from_data(result):
    qrcode = helpers.make_epc_qr(name=result['issuer'],
                                 iban=result['iban'],
                                 bic=result['bic'],
                                 amount=result['amount'],
                                 reference=result['reference'])
    return qrcode

def generate_qr_code_from_pdf(pdf_path, out_directory):
    result = extract_data_from_pdf(pdf_path)
    generate_qr_code_from_data(result, out_directory)

def generate_qr_code_from_data(result, out_directory):
    if result.get('paid', False):
        print('Invoice is marked as paid.')
    else:
        os.makedirs(out_directory, exist_ok=True)
        output_path = os.path.join(out_directory, 'qrcode.png')
        qrcode = make_qrcode_from_data(result)
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
    print(output)
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
    return result

def escape_sequence_from_invoice(pdf_path):
    result = extract_data_from_pdf(pdf_path)
    qrcode = make_qrcode_from_data(result)
    # Invert terminal colors. This is a crude way to get black on white output
    # instead of white on black background.
    sys.stdout.write("\033[;7m")
    qrcode.terminal(compact=True)
    # Reset terminal.
    sys.stdout.write("\033[0;0m\n")
    print(f"Amount: {result['amount']}")
    print(f"IBAN: {result['iban']}")
    print(f"Reference: {result['reference']}")

def insert_invoice(pdf_path):
    mmh3_hash = generate_hash_from_invoice(pdf_path)
    if db.is_hash_present(mmh3_hash):
        print(f"{pdf_path} is already present.")
    else:
        print(f"Inserting {pdf_path}...")
        _, original_filename = os.path.split(pdf_path)
        result = extract_data_from_pdf(pdf_path)
        if not result:
            db.insert_invoice(
                original_filename=original_filename,
                mmh3_hash=mmh3_hash,
                )
        else:
            db.insert_invoice(
                original_filename=original_filename,
                mmh3_hash=mmh3_hash,
                date=result['date'],
                invoice_number=result['invoice_number'],
                amount=result['amount'],
                paid='no',
                )

def insert_directory(directory):
    process_pdfs(directory, insert_invoice)

def generate_html_from_invoice(pdf_path, out_directory):
    result = process_pdf(pdf_path, out_directory)

    template_path = os.path.join(JINJA2_TEMPLATES_DIR, 'preview.html')
    template_dir, template_file = os.path.split(template_path)
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_file)

    content = {
        #"image_url": 'output.png',
        "image_url": pdf_path,
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

def check_directory(directory):
    def f(file_path):
        print(f"Processing {file_path}...")
        if not extract_data_from_pdf(file_path):
            print(f"Can't extract data from {file_path}.")
    process_pdfs(directory, f)

def process_pdfs(directory, processing_function):
    for root, _, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, '*.pdf'):
            file_path = os.path.join(root, filename)
            processing_function(file_path)

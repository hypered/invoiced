from invoice2data import extract_data
from invoice2data.extract.loader import read_templates

def extract_data_from_pdf(pdf_path):
    templates = read_templates('./templates/')
    result = extract_data(pdf_path, templates=templates)
    print(result)

def generate_qr_code_from_pdf(pdf_path):
    print("TODO")

from invoice2data import extract_data
from invoice2data.extract.loader import read_templates

if __name__ == '__main__':
  templates = read_templates('./templates/')
  result = extract_data('./pdfs/2023-04-09-ovh.pdf', templates=templates)
  print(result)

  print(type(result['amount']))

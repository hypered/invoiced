# Hide this warning:
#   PytzUsageWarning: The localize method is no longer necessary, as this time zone supports the fold attribute (PEP 495). For more details on migrating to a PEP 495-compliant implementation, see https://pytz-deprecation-shim.readthedocs.io/en/latest/migration.html
# TODO Revisit this later.
from pytz_deprecation_shim import PytzUsageWarning
from warnings import simplefilter
simplefilter(action='ignore', category=PytzUsageWarning)

import argparse
from . import core
from .server import start_server

def main():
    parser = argparse.ArgumentParser(description="Play with invoices.")
    subparsers = parser.add_subparsers(dest="command")

    extract_parser = subparsers.add_parser("extract", help="Extract data from a PDF file.")
    extract_parser.add_argument("pdf_path", help="Path to the PDF file.")

    qrcode_parser = subparsers.add_parser("qrcode", help="Generate a QR code from a PDF file.")
    qrcode_parser.add_argument("pdf_path", help="Path to the PDF file.")

    decode_parser = subparsers.add_parser("decode", help="Extract data from a QR code.")
    decode_parser.add_argument("image_path", help="Path to the image file.")

    image_parser = subparsers.add_parser("image", help="Convert a PDF to a PNG.")
    image_parser.add_argument("pdf_path", help="Path to the PDF file.")

    hash_parser = subparsers.add_parser("hash", help="Generate a hash for a given PDF.")
    hash_parser.add_argument("pdf_path", help="Path to the PDF file.")

    html_parser = subparsers.add_parser("html", help="Generate an HTML page for a given PDF.")
    html_parser.add_argument("pdf_path", help="Path to the PDF file.")

    serve_parser = subparsers.add_parser("serve", help="Run an HTTP server.")

    args = parser.parse_args()

    out_directory = "generated/local"

    if args.command == "extract":
        core.extract_data_from_pdf(args.pdf_path)
    elif args.command == "qrcode":
        core.generate_qr_code_from_pdf(args.pdf_path, out_directory)
    elif args.command == "decode":
        core.display_qr_code_content(args.image_path)
    elif args.command == "image":
        core.convert_pdf_to_png(args.pdf_path, out_directory)
    elif args.command == "hash":
        s = core.generate_hash_from_invoice(args.pdf_path)
        print(s)
    elif args.command == "html":
        core.generate_html_from_invoice(args.pdf_path, out_directory)
    elif args.command == "serve":
        start_server()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

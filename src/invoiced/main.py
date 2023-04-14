# Hide this warning:
#   PytzUsageWarning: The localize method is no longer necessary, as this time zone supports the fold attribute (PEP 495). For more details on migrating to a PEP 495-compliant implementation, see https://pytz-deprecation-shim.readthedocs.io/en/latest/migration.html
# TODO Revisit this later.
from pytz_deprecation_shim import PytzUsageWarning
from warnings import simplefilter
simplefilter(action='ignore', category=PytzUsageWarning)

import argparse
from . import core

def main():
    parser = argparse.ArgumentParser(description="Play with invoices.")
    subparsers = parser.add_subparsers(dest="command")

    extract_parser = subparsers.add_parser("extract", help="Extract data from a PDF file.")
    extract_parser.add_argument("pdf_path", help="Path to the PDF file.")

    qrcode_parser = subparsers.add_parser("qrcode", help="Generate a QR code from a PDF file.")
    qrcode_parser.add_argument("pdf_path", help="Path to the PDF file.")

    decode_parser = subparsers.add_parser("decode", help="Extract data from a QR code.")
    decode_parser.add_argument("image_path", help="Path to the image file.")

    args = parser.parse_args()

    if args.command == "extract":
        core.extract_data_from_pdf(args.pdf_path)
    elif args.command == "qrcode":
        core.generate_qr_code_from_pdf(args.pdf_path)
    elif args.command == "decode":
        core.display_qr_code_content(args.image_path)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

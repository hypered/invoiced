# Invoiced

This repository contains (mostly) Belgian-related templates to extract
structured data from invoices given as (unstructured) PDF files. The templates
are intended for the `invoice2data` open source Python library.

It also contains some code around `invoice2data` to make it easier to create
and test templates, and to show extracted data in a web page (including as a
SEPA Credit Transfer QR code).

# Development

We're using a Nix shell to bring the necessary dependencies (e.g. Python
libraries or the `pdftotext` binary) during development:

```
$ nix-shell
$ invoice2data --help
```

This provides for instance `invoice2data` and `pdftotext`.

# Writing templates

When adding a new template, it is easier to use the `invoice2data` command-line
tool in debug mode. See below. The `invoice2data` repository has a tutorial too.

# Extracting data from PDFs

We're using `invoice2data`.

"Templates" are YAML files describing how to extract data from text using
regexes. The text itself is obtained using e.g. `texttopdf`. Other ways to
obtain the text is possible (e.g. using Tesseract).

Multiple templates are tried on a given PDF. The output can be saved to a file
(for instance in JSON).

```
$ invoice2data \
  --debug \
  --exclude-built-in-templates \
  --template-folder ./templates/ \
  pdfs/2023-04-09-ovh.pdf
```

Note: Example PDFs are not included in the repository.

TODO Try Tesseract on (possibly scanned) PDFs.

## Notes

- `invoice2data` seems quite fragile, e.g. it tries to read a PDF after it
  failed to generate it.
- Monetary amounts are using the `float` type.
- Some fields are mandatory (`date`, `amount`, `invoice_number`) but other
  fields that are important to us can fail to be extracted with simply a
  warning. Code exploiting the data should check for those cases.
- We're using the non-official `comment:` field to try to add some information
  to our templates.

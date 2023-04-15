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

Note: It seems quite fragile, e.g. trying to read a PDF after failing to
generate it.

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

`invoice2data` can be used as a library.

The above command is similar to running the `bin/extract.py` script:

```
$ python bin/extract.py 2>/dev/null
```

Note: The amount is a `float`.

# Templates

`invoice2data` comes with some templates, but the Proximus one for instance
didn't work on our example PDF. If we can somehow ensure the templates "work",
we should upstream them.

We're using the non-official `comment:` field to try to add some information to
our templates.

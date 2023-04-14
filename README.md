# Invoiced

This is a repository to play around with some Python libraries to extract data
from invoices (received as PDFs) and/or generate and read SEPA Credit Transfert
QR codes.

# Development

We're using a Nix shell to bring the necessary dependencies (e.g. Python
libraries or the `pdftotext` binary).

```
$ nix-shell
```

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

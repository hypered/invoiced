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

# SQL

```
$ sqlite3 invoices.db < sql/create-invoices-table.sql
$ sqlite3 invoices.db ".schema invoices"
$ sqlite3 invoices.db "select * from invoices"
```

# Docker

A Docker image running `invoiced serve` with Gunicorn is provided:

```
$ nix-build docker.nix
$ docker load < result
$ docker run -p 8000:8000 invoiced:xxxx
```

Note: I didn't manage to get `convert` to run properly. The error when run
within the container:

```
$ docker run -v$(pwd):/src invoiced:qqyikanwalr3y0x07aq936896zagjpi7 convert -quality 100 -density 200 -colorspace sRGB '/src/pdfs/2023-01-09-proximus.pdf[0]' -flatten /src/output.png
convert: FailedToExecuteCommand `'gs' -sstdout=%stderr -dQUIET -dSAFER -dBATCH -dNOPAUSE -dNOPROMPT -dMaxBitmap=500000000 -dAlignToPixels=0 -dGridFitTT=2 '-sDEVICE=pngalpha' -dTextAlphaBits=4 -dGraphicsAlphaBits=4 '-r200x200' -dPrinted=false -dFirstPage=1 -dLastPage=1 '-sOutputFile=magick-YMX-n5OYS7EpIgG9fu04gS4I7nGNnCNl%d' '-fmagick-OwWeXniaYxuw2iAhuXsz-k1nZxBrwoWG' '-fmagick-QvORRBCAbGmU4AKh7VoxaEDlubJkI2qk'' (32512) @ error/ghostscript-private.h/ExecuteGhostscriptCommand/74.
convert: no images defined `/src/output.png' @ error/convert.c/ConvertImageCommand/3342.
```

When using `convert` on my host machine, but omitting `gs`, is very similar,
but has an additional `sh: line 1: gs: command not found` line:

```
$ convert -quality 100 -density 200 -colorspace sRGB 'pdfs/2023-01-09-proximus.pdf[0]' -flatten output.png
sh: line 1: gs: command not found
convert: FailedToExecuteCommand `'gs' -sstdout=%stderr -dQUIET -dSAFER -dBATCH -dNOPAUSE -dNOPROMPT -dMaxBitmap=500000000 -dAlignToPixels=0 -dGridFitTT=2 '-sDEVICE=pngalpha' -dTextAlphaBits=4 -dGraphicsAlphaBits=4 '-r200x200' -dPrinted=false -dFirstPage=1 -dLastPage=1 '-sOutputFile=/run/user/1000/magick-_f97AT5-L2DxpZYeSrj-LNLOgB8QW3b8%d' '-f/run/user/1000/magick-arJJP49wUA61JM7BoRTyPPj6kApH5gGZ' '-f/run/user/1000/magick-sLB3aFbLHxrGl-LUdJLCApxv9H6ugSt0'' (32512) @ error/ghostscript-private.h/ExecuteGhostscriptCommand/74.
convert: no images defined `output.png' @ error/convert.c/ConvertImageCommand/3342.
```

(Calling `gs` directly in the container does work.)

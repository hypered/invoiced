let
  pkgs = import <nixpkgs> {};
in
  pkgs.runCommand "dummy" {
    buildInputs = with pkgs; [
      python39
      python39Packages.jinja2
      python39Packages.mmh3
      python39Packages.pillow
      python39Packages.pyzbar
      python39Packages.qrcode
      (python39.pkgs.buildPythonApplication rec {
        pname = "invoice2data";
        version = "0.4.4";
        src = python.pkgs.fetchPypi {
          inherit pname version;
          hash = "sha256-S6xRdgKB9utmXVHsB8XIwIwlZ1Kfy2XKFGs8ekHj2vA=";
        };
        propagatedBuildInputs = with python39Packages; [
          dateparser
          pillow
          pytest-runner
          pyyaml
          setuptools-git

          pkgs.poppler_utils # For pdftotext.

          # For ocrmypdf and/or tesseract.
          #ocrmypdf
          #pkgs.imagemagick
          #pkgs.ghostscript
          #pkgs.tesseract
        ];
      })
      (python39.pkgs.buildPythonApplication rec {
        pname = "segno";
        version = "1.5.2";
        src = python.pkgs.fetchPypi {
          inherit pname version;
          hash = "sha256-mDQkspbmIYnXD8c0YM2UbPVty+grm9oYwGb8GyQ3HNw=";
        };
        propagatedBuildInputs = with python39Packages; [
        ];
      })
      pkgs.imagemagick
      pkgs.ghostscript
    ];
  } ""

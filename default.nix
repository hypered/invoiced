# This repeats much of shell.nix, but crucially uses buildPythonPackage instead
# of buildPythonApplication, otherwise the environments constructed with
# python39.withPackages or buildEnv are not able to load the modules in
# python (or gunicorn).

let
  pkgs = import <nixpkgs> {};

  invoice2data = pkgs.python39.pkgs.buildPythonPackage rec {
    pname = "invoice2data";
    version = "0.4.4";
    src = pkgs.python.pkgs.fetchPypi {
      inherit pname version;
      hash = "sha256-S6xRdgKB9utmXVHsB8XIwIwlZ1Kfy2XKFGs8ekHj2vA=";
    };
    propagatedBuildInputs = with pkgs.python39Packages; [
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
  };
  segno = pkgs.python39.pkgs.buildPythonPackage rec {
    pname = "segno";
    version = "1.5.2";
    src = pkgs.python.pkgs.fetchPypi {
      inherit pname version;
      hash = "sha256-mDQkspbmIYnXD8c0YM2UbPVty+grm9oYwGb8GyQ3HNw=";
    };
    propagatedBuildInputs = with pkgs.python39Packages; [
    ];
  };
  invoiced = pkgs.python39.pkgs.buildPythonPackage rec {
    pname = "invoiced";
    version = "0.1.0";
    src = ./.;
    propagatedBuildInputs = with pkgs.python39Packages; [
      invoice2data
      flask
      jinja2
      mmh3
      pillow
      pytz-deprecation-shim
      pyzbar
      qrcode
      segno
      setuptools
    ];
  };
  invoiced-env = pkgs.buildEnv {
    name = "invoiced-env";
    paths = [
      (pkgs.python39.withPackages (ps: [ ps.gunicorn invoiced ]))
    ];
  };
in
{
  inherit invoiced invoiced-env;
  shell = pkgs.mkShell {
    buildInputs = [ invoiced-env ];
  };
}

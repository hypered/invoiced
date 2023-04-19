{ pkgs ? import <nixpkgs> { }
}:

let
  invoiced-env = (import ./.).invoiced-env;
  invoiced-jinja2-templates = (import ./.).invoiced-jinja2-templates;
  invoiced-invoice2data-templates = (import ./.).invoiced-invoice2data-templates;
in
pkgs.dockerTools.buildImage {
  name = "invoiced";
  contents = [ invoiced-env ];
  runAsRoot = ''
    #!${pkgs.runtimeShell}
    mkdir -p /run/invoiced/uploads
    mkdir -p /run/invoiced/generated
  '';
  config = {
    WorkingDir = "/run/invoiced";
    Cmd = [
      "${invoiced-env}/bin/gunicorn"
      "--access-logfile" "-"
      "--bind" "0.0.0.0" # So that Gunicorn accepts connections from
                         # outside the container.
      "invoiced.server:app"
      ];
    Env = [
      "JINJA2_TEMPLATES_DIR=${invoiced-jinja2-templates}"
      "YAML_TEMPLATES_DIR=${invoiced-invoice2data-templates}"
      "UPLOAD_DIR=/run/invoiced/uploads"
    ];
  };
}

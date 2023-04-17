{ pkgs ? import <nixpkgs> { }
}:

let
  invoiced-env = (import ./.).invoiced-env;
in
pkgs.dockerTools.buildImage {
  name = "invoiced";
  config = {
    Cmd = [
      "${invoiced-env}/bin/gunicorn"
      "--access-logfile" "-"
      "--bind" "0.0.0.0" # So that Gunicorn accepts connections from
                         # outside the container.
      "invoiced.server:app"
      ];
  };
}

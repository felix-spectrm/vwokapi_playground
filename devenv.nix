{
  pkgs,
  lib,
  config,
  inputs,
  ...
}:

{
  packages = [ pkgs.ruff ];

  dotenv.enable = true;

  treefmt = {
    enable = true;
    config.programs = {
      nixfmt.enable = true;
      ruff-check.enable = true;
      ruff-format.enable = true;
    };
  };

  git-hooks.hooks = {
    treefmt.enable = true;
  };

  languages.python = {
    enable = true;
    venv.enable = true;
    lsp.package = pkgs.basedpyright;
    uv = {
      enable = true;
      sync = {
        enable = true;
        allGroups = true;
      };
    };
  };

  tasks."python:typecheck" = {
    description = "Type-check the codebase with basedpyright";
    exec = "${lib.getExe pkgs.basedpyright} .";
    after = [ "devenv:python:uv" ];
  };
}

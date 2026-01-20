{
  pkgs,
  config,
  ...
}: {
  # https://devenv.sh/packages/
  packages = [(config.languages.python.import ./. {})];

  # https://devenv.sh/languages/
  languages.python = {
    enable = true;
    package = pkgs.python312;
    directory = "./.";
    uv.enable = true;
  };
  # https://devenv.sh/basics/
  enterShell = ''
    echo "xls2latex development environment"
    echo "Package available: xls2latex"
  '';

  # https://devenv.sh/tasks/
  # tasks = {
  #   "myproj:setup".exec = "mytool build";
  #   "devenv:enterShell".after = [ "myproj:setup" ];
  # };

  # https://devenv.sh/tests/
  enterTest = ''
    echo "Running tests"
    git --version | grep --color=auto "${pkgs.git.version}"
  '';

  # https://devenv.sh/git-hooks/
  # git-hooks.hooks.shellcheck.enable = true;

  # See full reference at https://devenv.sh/reference/options/
}

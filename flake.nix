# flake made with nix flake new -t "github:serokell/nix-templates#python-poetry2nix" xls2latex

{
  description = "xls2latex converts xls(x) worksheets to LaTeX tables (best used with pandoc(omatic))";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        customOverrides = self: super: {
          # Overrides go here
        };

        app = pkgs.poetry2nix.mkPoetryApplication {
          projectDir = ./.;
          overrides =
            [ pkgs.poetry2nix.defaultPoetryOverrides customOverrides ];
        };

        packageName = "xls2latex";
      in {
        packages.${system}.${packageName} = app;

        defaultPackage = app;

        devShell = pkgs.mkShell {
          buildInputs = with pkgs;[
            poetry
            (pkgs.python3.withPackages (p: with p; [ pylint ]))
          ];
          # inputsFrom = builtins.attrValues self.packages.${system};
        };
      });
}

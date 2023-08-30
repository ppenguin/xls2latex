# flake made with nix flake new -t "github:serokell/nix-templates#python-poetry2nix" xls2latex

{
  description = "xls2latex converts xls(x) worksheets to LaTeX tables (best used with pandoc(omatic))";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.05";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
  {
    # Nixpkgs overlay providing the application
    overlay = nixpkgs.lib.composeManyExtensions [
      poetry2nix.overlay
      (final: prev: {

        xls2latex = import ./default.nix { pkgs = prev; };

        xls2latex-devenv = prev.poetry2nix.mkPoetryEnv {
          projectDir = ./.;
          # overrides = [ prev.poetry2nix.defaultPoetryOverrides ];
        };

      })
    ];
  } // flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; overlays = [ self.overlay ];};
        packageName = "xls2latex";
      in {
        packages.${system}.${packageName} = pkgs.xls2latex;
        defaultPackage = pkgs.xls2latex;

        devShell = pkgs.mkShell {
          buildInputs = with pkgs;[
            xls2latex-devenv
            poetry
            (pkgs.python3.withPackages (p: with p; [ pylint ]))
          ];
        };
      });
}

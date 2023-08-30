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

        xls2latex = prev.poetry2nix.mkPoetryApplication {
          projectDir = ./.;
          # overrides = [ prev.poetry2nix.defaultPoetryOverrides ];
          meta = with nixpkgs.lib; {
            description = "Converts xls(x) worksheets to LaTeX tables (best used with pandoc(omatic))";
            longDescription = ''
              Xls2latex is a python program that can be used to include tables from xls(x) worksheet in LaTeX documents.
              It can be used transparently in (e.g.) pandoc md-to-latex-to-pdf workflows.
            '';
            homepage = "https://github.com/ppenguin/xls2latex";
            license = licenses.agpl3Plus;
            maintainers = with maintainers; [ ppenguin ];
            platforms = platforms.all;
          };
        };

        xls2latex-devenv = prev.poetry2nix.mkPoetryEnv {
          projectDir = ./.;
          overrides =
            [ prev.poetry2nix.defaultPoetryOverrides ];
        };

      })
    ];
  } // flake-utils.lib.eachDefaultSystem (system:
      let
        # nixpkgs.overlays = [ self.overlay ];
        # pkgs = nixpkgs.legacyPackages.${system};
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

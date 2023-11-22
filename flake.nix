{
  description = "xls2latex converts xls(x) worksheets to LaTeX tables (best used with pandoc(omatic))";

  inputs = {
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = inputs@{ self, nixpkgs, flake-utils, poetry2nix }:
  {
    # Nixpkgs overlay providing the application
    overlay = nixpkgs.lib.composeManyExtensions [
      (final: prev: {
        xls2latex = import ./default.nix { pkgs = prev; };
        # xls2latex-devenv = final.poetry2nix.mkPoetryEnv {
        #   projectDir = ./.;
        #   # overrides = [ prev.poetry2nix.defaultPoetryOverrides ];
        # };
        # poetry2nix = poetry2nix.packages.${prev.system};
      })
    ];
  } // flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs { inherit system; overlays = [ self.overlay ];};
      inherit (poetry2nix.packages.${system}.poetry2nix) mkPoetryApplication mkPoetryEnv;
      packageName = "xls2latex";
    in
    {
      packages.${system}.${packageName} = pkgs.xls2latex;
      defaultPackage = pkgs.xls2latex;

      devShell = pkgs.mkShell {
        buildInputs = with pkgs;[
          # xls2latex-devenv
          (mkPoetryEnv { projectDir = self; }).env
          poetry
          (pkgs.python3.withPackages (p: with p; [ pylint ]))
        ];
      };
    }
  );
}

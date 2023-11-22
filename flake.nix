{
  description = "xls2latex converts xls(x) worksheets to LaTeX tables (best used with pandoc(omatic))";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    # nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        # see https://github.com/nix-community/poetry2nix/tree/master#api for more functions and examples.
        pkgs = nixpkgs.legacyPackages.${system};
        inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication;
        xls2latex = pkgs.callPackage ./default.nix { inherit mkPoetryApplication; };# mkPoetryApplication { projectDir = self; };
      in

      {
        overlays.default = final: prev: {
          inherit xls2latex;
        };

        packages = rec {
          # xls2latex = pkgs.callPackage ./default.nix { inherit mkPoetryApplication; inherit (pkgs) lib; };# mkPoetryApplication { projectDir = self; };
          inherit xls2latex;
          default = /* self.packages. */xls2latex;
        };

        devShells.default = pkgs.mkShell {
          inputsFrom = [ xls2latex ];
          packages = [ pkgs.poetry ];
        };
      });
}

{ pkgs ? import <nixpkgs> { } }:

pkgs.poetry2nix.mkPoetryApplication {
  projectDir = ./.;
  python = pkgs.python3;
  meta = with pkgs.lib; {
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
}
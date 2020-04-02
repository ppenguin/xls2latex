# xls2latex
Python script to convert read tables from xls(x) files and output LaTeX tables.
Based on [excel2latexviapython](https://github.com/michaelkirker/excel2latexviapython) by Michael Kirker.

## Status
To be considered **alpha** quality! It works for my use case but testing has been very limited, so YMMV.
Feel free to make improvements!

## Features
Outputs valid `LaTeX` code for tables from `Excel/LibreOffice` workbooks (one table per worksheet) while
honoring the following properties in the worksheet:
 - colours (untested)
 - number format
 - alignment (even for individual cells!)
 - borders.

Additionally, for multi-line cells needing wrapped text, you can now set the column widths on the 
command line (since `openpyxl` seems to incorrectly report column widths).

## Prerequisites

Needs (at least) the following `LaTeX` packages:
- `longtable`
- `array`
- `xcolor`
- `caption`
- `multirow`
- `multicolumn`

## Usage
You can use `xls2tex.py` stand alone to read `myfile.xlsx` and pipe the output to `mytable.tex` for inclusion 
in a `LaTeX` document.

```
/path/to/xls2tex.py -f myfile.xlsx > mytable.tex
```
Get the possible command line options by executing without arguments `xls2tex.py`.

A more convenient use, however, is to use call the script from `LaTeX` by using piped input:

```
\input{|"xls2tex.py -f myfile.xlsx"}
```
You can do this either from your `LaTeX` workflow or from your `pandoc` workflow. This requires activation 
of shell command execution (off by default for security reasons), in the `pandoc` case e.g.:

```
pandoc --filter=pandoc-citeproc --filter=pandoc-crossref --filter=pandoc-xnos \
    --pdf-engine=xelatex --pdf-engine-opt=-shell-escape \
    -i testdoc.md -o testdoc.pdf
```
where `testdoc.md` contains the above `\input` command.

## Installation
No user-friendly method yet, just copy/clone.
I used a `poetry` environment, so you could do the same to handle dependencies.

# Broader Background
## Why?
### Reason
The main reason for developing this script is to get around the severe limitation of markdown tables in terms of 
formatting and to automate inclusion of an effective workflow to author tables. (Let's face it, making tables is
still by far the easiest using office-like software.)

But, if, like me, you replaced your documentation workflow to make e.g. letters, reports, quotations, etc. 
from well-known office software to markdown, you may be faced with the challenge of including these external tables.

Since for this workflow my output format is still the "traditional" `pdf`, it makes sense to use `LaTeX` as an intermediate format.
Enter [Pandoc](https://pandoc.org/).

## How?
### Workflow
If you want to leverage the `markdown - pandoc LaTeX - pdf` workflow to the fullest, it is advisable to fine-tune the workflow
in such a way, that you only need to configure each document type once (customised templates). The objective being that you can
write any document in `markdown` completely without leaving your editor, and generate a `pdf` with a generic one-line command.
Enter [pandocomatic](https://github.com/htdebeer/pandocomatic).

After setting up `pandoc` and `pandocomatic` (and your custom templates, which are called from the pandocomatic config file 
depending on which document type you choose in your document's `YAML` header), you can use one single invocation of 
`pandocomatic` with your `md` file to automatically generate the desired output.

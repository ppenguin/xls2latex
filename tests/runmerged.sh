#! /usr/bin/env bash

python ../xls2latex.py -f merged.xlsx -e > merged.tex

pandoc --filter=pandoc-xnos --filter=pandoc-crossref  \
    --template=pandoc_template_min.latex --pdf-engine=xelatex --pdf-engine-opt=-shell-escape --verbose \
    -i merged.md -o merged.pdf && open merged.pdf

#pandoc --filter=pandoc-xnos --filter=pandoc-crossref \
#    -V templatepath=/Users/jeroen/.pandoc/templates/1nnovatio --template=/Users/jeroen/.pandoc/templates/1nnovatio/1nnoquote.latex --pdf-engine=xelatex --pdf-engine-opt=-shell-escape \
#    -i merged.md -o merged.pdf && open merged.pdf
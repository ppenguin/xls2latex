#! /usr/bin/env bash

# pandoc --filter=pandoc-xnos --filter=pandoc-crossref \
#    --template=pandoc_template_min.latex --pdf-engine=xelatex --pdf-engine-opt=-shell-escape \
#    -i testdoc.md -o testdoc.pdf && open testdoc.pdf

pandoc --filter=pandoc-xnos --filter=pandoc-crossref \
    -V templatepath=/Users/jeroen/.pandoc/templates/1nnovatio --template=/Users/jeroen/.pandoc/templates/1nnovatio/1nnoquote.latex --pdf-engine=xelatex --pdf-engine-opt=-shell-escape \
    -i testdoc.md -o testdoc.pdf && open testdoc.pdf
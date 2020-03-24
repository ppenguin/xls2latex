#! /usr/bin/env bash

pandoc --filter=pandoc-citeproc --filter=pandoc-crossref --filter=pandoc-xnos \
    --pdf-engine=xelatex --pdf-engine-opt=-shell-escape \
    -i testdoc.md -o testdoc.pdf
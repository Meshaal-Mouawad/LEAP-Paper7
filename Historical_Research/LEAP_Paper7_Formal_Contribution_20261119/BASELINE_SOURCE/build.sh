#!/bin/sh
set -eu
pdflatex -interaction=nonstopmode -halt-on-error Paper7.tex
if command -v bibtex8 >/dev/null 2>&1; then
  bibtex8 Paper7
elif command -v bibtex >/dev/null 2>&1; then
  bibtex Paper7
else
  echo 'BibTeX not available: using supplied Paper7.bbl' >&2
fi
pdflatex -interaction=nonstopmode -halt-on-error Paper7.tex
pdflatex -interaction=nonstopmode -halt-on-error Paper7.tex

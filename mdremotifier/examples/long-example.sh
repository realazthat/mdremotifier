#!/bin/bash
# https://gist.github.com/mohanpedala/1e2ff5661761d3abd0385e8223e16425
set -e -x -v -u -o pipefail



python -m mdremotifier.cli \
  -i "mdremotifier/examples/LONG-EXAMPLE.md" \
  --url-prefix https://raw.githubusercontent.com/realazthat/mdremotifier/master/ \
  -o "mdremotifier/examples/LONG-EXAMPLE.remotified.md"

#!/bin/bash
# https://gist.github.com/mohanpedala/1e2ff5661761d3abd0385e8223e16425
set -e -x -v -u -o pipefail

# SNIPPET_START
python -m mdremotifier.cli \
  -i "mdremotifier/examples/EXAMPLE.md" \
  --url-prefix https://github.com/realazthat/mdremotifier/blob/master/ \
  --img-url-prefix https://raw.githubusercontent.com/realazthat/mdremotifier/master/ \
  -o "mdremotifier/examples/EXAMPLE.remotified.md"
# SNIPPET_END

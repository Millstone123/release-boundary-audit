#!/bin/sh
set -eu
PYTHONPATH=. python3 -m unittest discover -s tests -v
PYTHONPATH=. python3 -m release_boundary_audit . >/dev/null

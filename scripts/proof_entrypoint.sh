#!/bin/sh
# Repeatedly runs mediasorter.py, sleeping RUN_INTERVAL_SECONDS between passes.
set -e

INTERVAL="${RUN_INTERVAL_SECONDS:-86400}"
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

while true; do
    python "$SCRIPT_DIR/scripts/make_proofs.py"
    sleep "$INTERVAL"
done

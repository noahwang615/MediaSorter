#!/bin/sh
set -e

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

echo "Triggering MediaSorter manual proof generation in Docker..."
docker compose run --rm --entrypoint python mediasorter scripts/make_proofs.py
echo "Manual proof generation complete."

#!/bin/sh
set -e

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

echo "Triggering MediaSorter manual sort in Docker..."
if docker compose exec mediasorter python scripts/mediasorter.py 2>/dev/null; then
    echo "Manual sort complete."
else
    echo "Container not running, running one-shot container..."
    docker compose run --rm --entrypoint python mediasorter scripts/mediasorter.py
    echo "Manual sort complete."
fi

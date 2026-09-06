#!/bin/bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Python was not found. Run the local installer first." >&2
  exit 1
fi

cd "$PROJECT_ROOT"
"$PYTHON_BIN" scripts/migrate_to_raw.py "$@"
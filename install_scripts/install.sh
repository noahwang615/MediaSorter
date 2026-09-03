#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALLER="$SCRIPT_DIR/install.py"

PYTHON_BIN=""

for candidate in python3.11 python3.12 python3; do
  if command -v "$candidate" >/dev/null 2>&1; then
    version="$($candidate -c 'import sys; print(f"{sys.version_info[0]}.{sys.version_info[1]}")' 2>/dev/null || true)"
    if [ -n "$version" ]; then
      major="${version%%.*}"
      minor="${version#*.}"
      if [ "$major" -gt 3 ] || { [ "$major" -eq 3 ] && [ "$minor" -ge 11 ]; }; then
        PYTHON_BIN="$candidate"
        break
      fi
    fi
  fi
done

if [ -z "$PYTHON_BIN" ]; then
  echo "Python 3.11 or newer was not found. Please install Python 3.11+ first."
  exit 1
fi

echo "Using: $PYTHON_BIN"
exec "$PYTHON_BIN" "$INSTALLER"

#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

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

PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REQ_FILE="$PROJECT_ROOT/scripts/requirements.txt"
ENV_FILE="$PROJECT_ROOT/.env"

echo "Checking if pip is updated"
"$PYTHON_BIN" -m pip install --upgrade pip

echo "Installing dependencies from $REQ_FILE"
"$PYTHON_BIN" -m pip install --no-cache-dir -r "$REQ_FILE"

echo "Verifying dependencies"
"$PYTHON_BIN" -c "import PIL, dotenv, pillow_heif; print('Dependencies verified')"

if ! command -v ffprobe >/dev/null 2>&1; then
  echo "ffprobe is not installed. Please install ffmpeg first."
  exit 1
fi

prompt_path() {
  local var_name="$1"
  local prompt_text="$2"
  local fallback_default="$3"
  local default_val=""
  if [ -f "$ENV_FILE" ]; then
    default_val=$(grep "^${var_name}=" "$ENV_FILE" | cut -d '=' -f2-)
  fi
  default_val="${default_val:-$fallback_default}"

  local input
  read -r -p "$prompt_text [$default_val]: " input
  input="${input:-$default_val}"
  if [ -z "$input" ]; then
    echo "Error: $var_name cannot be empty." >&2
    exit 1
  fi

  mkdir -p "$input"
  echo "$var_name=$input"
}

echo
echo "Configuring MediaSorter paths (used by mediasorter.py via .env)"
MEDIA_SRC_LINE=$(prompt_path MEDIA_SRC "Media dump source folder" "$PROJECT_ROOT/data/mediadump")
PHOTO_DEST_LINE=$(prompt_path PHOTO_DEST "Photo destination folder" "$PROJECT_ROOT/data/photos")
VIDEO_DEST_LINE=$(prompt_path VIDEO_DEST "Video destination folder" "$PROJECT_ROOT/data/videos")

{
  echo "$MEDIA_SRC_LINE"
  echo "$PHOTO_DEST_LINE"
  echo "$VIDEO_DEST_LINE"
  echo "RUN_INTERVAL_SECONDS=3600"
} > "$ENV_FILE"

echo
echo "Wrote $ENV_FILE"
echo "Done. Run it with: $PYTHON_BIN $PROJECT_ROOT/scripts/mediasorter.py"

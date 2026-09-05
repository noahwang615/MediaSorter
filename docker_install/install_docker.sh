#!/bin/bash
# Interactive setup: collects host paths, writes .env, builds the Docker image.
set -e

cd "$(dirname "$0")/.."

ENV_FILE=".env"

prompt_path() {
    local var_name="$1"
    local prompt_text="$2"
    local default_val=""
    if [ -f "$ENV_FILE" ]; then
        default_val=$(grep "^${var_name}=" "$ENV_FILE" | cut -d '=' -f2-)
    fi

    local input
    read -r -p "$prompt_text${default_val:+ [$default_val]}: " input
    input="${input:-$default_val}"

    if [ -z "$input" ]; then
        echo "Error: $var_name cannot be empty." >&2
        exit 1
    fi

    mkdir -p "$input"
    echo "$var_name=$input"
}

echo "MediaSorter Docker setup"
echo "Enter absolute host paths for each directory (created if missing)."
echo

MEDIA_SRC_LINE=$(prompt_path MEDIA_SRC "Media dump source folder")
PHOTO_DEST_LINE=$(prompt_path PHOTO_DEST "Photo destination folder")
VIDEO_DEST_LINE=$(prompt_path VIDEO_DEST "Video destination folder")

DEFAULT_INTERVAL=3600
if [ -f "$ENV_FILE" ]; then
    DEFAULT_INTERVAL=$(grep "^RUN_INTERVAL_SECONDS=" "$ENV_FILE" | cut -d '=' -f2-)
    DEFAULT_INTERVAL="${DEFAULT_INTERVAL:-3600}"
fi
read -r -p "Run interval in seconds [$DEFAULT_INTERVAL]: " INTERVAL_INPUT
INTERVAL_INPUT="${INTERVAL_INPUT:-$DEFAULT_INTERVAL}"

DEFAULT_PROOF_ENABLE="n"
if [ -f "$ENV_FILE" ] && grep -q "^COMPOSE_PROFILE=proof$" "$ENV_FILE"; then
    DEFAULT_PROOF_ENABLE="y"
fi
read -r -p "Enable proof generation service? (y/N) (default: $DEFAULT_PROOF_ENABLE): " PROOF_ENABLE_INPUT
PROOF_ENABLE_INPUT="${PROOF_ENABLE_INPUT:-$DEFAULT_PROOF_ENABLE}"

if [ "$PROOF_ENABLE_INPUT" = "y" ] || [ "$PROOF_ENABLE_INPUT" = "Y" ]; then
    COMPOSE_PROFILE_LINE="COMPOSE_PROFILE=proof"
    
    DEFAULT_PROOF_INTERVAL=86400
    if [ -f "$ENV_FILE" ]; then
        DEFAULT_PROOF_INTERVAL=$(grep "^PROOF_INTERVAL_SECONDS=" "$ENV_FILE" | cut -d '=' -f2-)
        DEFAULT_PROOF_INTERVAL="${DEFAULT_PROOF_INTERVAL:-86400}"
    fi
    read -r -p "Proof generation interval in seconds [$DEFAULT_PROOF_INTERVAL]: " PROOF_INTERVAL_INPUT
    PROOF_INTERVAL_INPUT="${PROOF_INTERVAL_INPUT:-$DEFAULT_PROOF_INTERVAL}"
    PROOF_INTERVAL_LINE="PROOF_INTERVAL_SECONDS=$PROOF_INTERVAL_INPUT"
fi

{
    echo "$MEDIA_SRC_LINE"
    echo "$PHOTO_DEST_LINE"
    echo "$VIDEO_DEST_LINE"
    echo "RUN_INTERVAL_SECONDS=$INTERVAL_INPUT"
    if [ "$PROOF_ENABLE_INPUT" = "y" ] || [ "$PROOF_ENABLE_INPUT" = "Y" ]; then
        echo "$COMPOSE_PROFILE_LINE"
        echo "$PROOF_INTERVAL_LINE"
    fi
} > "$ENV_FILE"

echo
echo "Wrote $ENV_FILE"
echo "Building Docker image..."
docker compose build

echo
echo "Done. Start the container with: docker compose up -d (or 'make up')"

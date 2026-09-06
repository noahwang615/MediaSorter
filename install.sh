#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$SCRIPT_DIR/data/mediadump" "$SCRIPT_DIR/data/photos" "$SCRIPT_DIR/data/videos"

echo "MediaSorter installer"
echo "1) Local install"
echo "2) Docker install"
read -r -p "Choose an option [1/2]: " choice

case "$choice" in
  1) exec "$SCRIPT_DIR/local_install/install_local.sh" ;;
  2) exec "$SCRIPT_DIR/docker_install/install_docker.sh" ;;
  *) echo "Invalid choice." >&2; exit 1 ;;
esac

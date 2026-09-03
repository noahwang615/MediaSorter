#!/usr/bin/env python3

import sys
import subprocess
from pathlib import Path

MIN_VERSION = (3, 11)
ROOT = Path(__file__).resolve().parent
PROJECT_BASE = ROOT.parent
REQ_FILE = PROJECT_BASE / "install_scripts" / "requirements.txt"


def main():
    if sys.version_info < MIN_VERSION:
        raise SystemExit(
            f"MediaSorter requires Python {MIN_VERSION[0]}.{MIN_VERSION[1]} or newer."
        )

    if not REQ_FILE.exists():
        raise SystemExit(f"Missing requirements file: {REQ_FILE}")

    print(f"Using Python: {sys.executable}")
    print(f"Installing from: {REQ_FILE}")

    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(REQ_FILE)])

    try:
        subprocess.check_call(
            [sys.executable, "-c", "import PIL, pillow_heif; print('Dependencies verified')"]
        )
    except subprocess.CalledProcessError as e:
        raise SystemExit("Dependency verification failed.") from e

    print("Installation completed successfully.")


if __name__ == "__main__":
    main()

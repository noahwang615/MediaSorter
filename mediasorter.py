# Dump all file in /mediadump to $PHOTO_PATH/yyyy/mm/* or $VIDEO_PATH/yyyy/mm/*

import os
import shutil
import mimetypes
import subprocess
import json
import logging
import sys
from datetime import datetime

from pillow_heif import register_heif_opener
from PIL import Image
from PIL.ExifTags import TAGS

# Register HEIF support for Pillow (HEIC/HEIF decode)
register_heif_opener()

# =======  CONFIGURATION START =======

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_BASE = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

LOG_DIR = os.path.join(SCRIPT_DIR, "test_logs")
LOG_FILE = os.path.join(LOG_DIR, "mediasorter_test.log")
DATE_FALLBACK = "0000-00-00"

########## USER EDIT PATHS BELOW - CHANGE THESE FOR YOUR SETUP ##########

# SOURCE_DIR = os.path.join(PROJECT_BASE, "mediadump")      <-- Uncomment if using default path (mediadump folder in project root)
# SOURCE_DIR = "path/to/your/mediadump_directory"           <-- Uncomment if using custom path

IMAGE_TARGET_DIR = "path/to/your/image_target_directory"  # <-- Change this to your desired image target path
VIDEO_TARGET_DIR = "path/to/your/video_target_directory"  # <-- Change this to your desired video target path

"""
Here's an example how my path works. I store all my media in a Synology instance, so my Media_AutoSort is inside Synology looking for those directories
SOURCE_DIR = "/volume1/homes/mediadump"
IMAGE_TARGET_DIR = "/volume1/homes/images"
VIDEO_TARGET_DIR = "/volume1/homes/video" 
"""

########## USER EDIT PATHS BELOW - CHANGE THESE FOR YOUR SETUP ##########

# =======  CONFIGURATION END =======


# Logging setup
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "mediasorter_test.log")),
        logging.StreamHandler()
    ]
)

def check_dependencies() -> None:
    """
    Checks if Pillow, pillow-heif, and ffprobe are available.
    """
    try:
        import PIL  # noqa: F401
    except ImportError:
        logging.error("Pillow is not installed. Please run 'pip install Pillow'.")
        sys.exit(1)

    try:
        import pillow_heif  # noqa: F401
    except ImportError:
        logging.error("pillow-heif is not installed. Please run 'pip install pillow-heif'.")
        sys.exit(1)

    if not shutil.which("ffprobe"):
        logging.error("ffprobe (from ffmpeg) is not installed or not in PATH.")
        logging.error("Please install ffmpeg and ensure ffprobe is available.")
        sys.exit(1)

# ===== Media type checks =====

def is_photo(file_path):
    mime_type, _ = mimetypes.guess_type(file_path.lower())
    return mime_type and mime_type.startswith("image")

def is_video(file_path):
    mime_type, _ = mimetypes.guess_type(file_path.lower())
    return mime_type and mime_type.startswith("video")

# ===== Helper functions =====

def parse_exif_date(exif_data) -> str | None:
    """
    Prefer original capture date, then common EXIF fallbacks.
    EXIF datetime format is usually: YYYY:MM:DD HH:MM:SS
    """
    if not exif_data:
        return None

    preferred_tags = ("DateTimeOriginal", "DateTimeDigitized", "DateTime")
    tag_name_to_value = {}

    for tag, value in exif_data.items():
        tag_name = TAGS.get(tag)
        if isinstance(value, str) and tag_name:
            tag_name_to_value[tag_name] = value

    for tag_name in preferred_tags:
        value = tag_name_to_value.get(tag_name)
        if value:
            return value.split()[0].replace(":", "-")

    return None

def get_photo_date(photo_path: str) -> str:
    try:
        with Image.open(photo_path) as img:
            exif_data = img.getexif()
        parsed = parse_exif_date(exif_data)
        if parsed:
            return parsed
        logging.warning("No usable EXIF datetime found for %s", photo_path)
    except Exception as e:
        logging.warning("EXIF error for %s: %s", photo_path, e)

    try:
        return datetime.fromtimestamp(os.path.getctime(photo_path)).strftime("%Y-%m-%d")
    except Exception as e:
        logging.warning("Timestamp error for %s: %s", photo_path, e)
        return DATE_FALLBACK

# use ffprobe to get video creation time
def get_video_date(video_path: str) -> str:
    try:
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_entries", "format_tags=creation_time",
            video_path,
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        metadata = json.loads(result.stdout or "{}")
        creation_time = metadata.get("format", {}).get("tags", {}).get("creation_time")
        if creation_time:
            return creation_time.split("T")[0]
    except Exception as e:
        logging.exception("ffprobe error for %s: %s", video_path, e)

    try:
        return datetime.fromtimestamp(os.path.getctime(video_path)).strftime("%Y-%m-%d")
    except Exception as e:
        logging.warning("Timestamp error for %s: %s", video_path, e)
        return DATE_FALLBACK

# Function to generate a unique filename if a duplicate exists
def get_unique_filename(directory, filename):
    base, ext = os.path.splitext(filename)
    counter = 2
    new_filename = filename

    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base}_{counter}{ext}"
        counter += 1

    return new_filename

# Function to get media date based on type
def get_media_date(file_path: str) -> str:
    if is_photo(file_path):
        return get_photo_date(file_path)
    elif is_video(file_path):
        return get_video_date(file_path)
    return DATE_FALLBACK

# ===== Main processing function =====

def process_file(file_path: str) -> str:
    if is_photo(file_path):
        target_dir = IMAGE_TARGET_DIR
    elif is_video(file_path):
        target_dir = VIDEO_TARGET_DIR
    else:
        logging.info("Skipping unsupported file type: %s", os.path.basename(file_path))
        return "skipped"

    date = get_media_date(file_path)
    if "-" not in date or len(date.split("-")) < 2:
        logging.warning("Skipping %s due to invalid date: %s", os.path.basename(file_path), date)
        return "skipped"

    year, month = date.split("-")[:2]
    final_folder = os.path.join(target_dir, year, month)
    os.makedirs(final_folder, exist_ok=True)

    new_filename = get_unique_filename(final_folder, os.path.basename(file_path))
    destination = os.path.join(final_folder, new_filename)

    try:
        shutil.move(file_path, destination)
        logging.info("Moved %s to %s as %s", os.path.basename(file_path), final_folder, new_filename)
        return "moved"
    except Exception:
        logging.exception("Failed to move %s to %s", os.path.basename(file_path), destination)
        return "failed"

# ===== Entry Point =====

def main() -> None:
    check_dependencies()

    logging.info("Starting MediaSorter")
    logging.info("Source directory: %s", SOURCE_DIR)
    logging.info("Image target directory: %s", IMAGE_TARGET_DIR)
    logging.info("Video target directory: %s", VIDEO_TARGET_DIR)

    if not os.path.isdir(SOURCE_DIR):
        logging.error("Source directory does not exist: %s", SOURCE_DIR)
        sys.exit(1)

    moved = 0
    skipped = 0
    failed = 0

    try:
        for item in os.listdir(SOURCE_DIR):
            item_path = os.path.join(SOURCE_DIR, item)
            if not os.path.isfile(item_path):
                continue

            result = process_file(item_path)
            if result == "moved":
                moved += 1
            elif result == "failed":
                failed += 1
            else:
                skipped += 1
    except Exception:
        logging.exception("Unexpected failure while scanning %s", SOURCE_DIR)
        sys.exit(1)

    logging.info("Finished MediaSorter: moved=%d skipped=%d failed=%d", moved, skipped, failed)


if __name__ == "__main__":
    main()
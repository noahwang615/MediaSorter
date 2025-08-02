# Dump all file in /mediadump to $PHOTO_PATH/yyyy/mm/* or $VIDEO_PATH/yyyy/mm/*

import os
import shutil
import mimetypes
import subprocess
import json
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
import logging
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')

def check_dependencies() -> None:
    """
    Checks if Pillow and ffprobe are installed.
    Exits the script if any required dependency is missing.
    """
    try:
        import PIL  # should be available if Pillow is installed
    except ImportError:
        logging.error("Pillow is not installed. Please run 'pip install Pillow'.")
        sys.exit(1)

    if not shutil.which("ffprobe"):
        logging.error("ffprobe (from ffmpeg) is not installed or not in PATH.")
        logging.error("Please install ffmpeg and ensure ffprobe is available.")
        sys.exit(1)

# Source and Target directories | Users: change these paths for your setup
SOURCE_DIR = "/Users/noahwang/Development/MediaSorter/mediadump"
IMAGE_TARGET_DIR = "/Users/noahwang/python_test/phototarget"
VIDEO_TARGET_DIR = "/Users/noahwang/python_test/videotarget"

""" 

Here's an example how my path works. I store all my media in a Synology instance, so my Media_AutoSort is inside Synology looking for those directories
SOURCE_DIR = "/volume1/homes/media_sort"
IMAGE_TARGET_DIR = "/volume1/homes/images"
VIDEO_TARGET_DIR = "/volume1/homes/video" 

"""

# GET creation date from EXIF data (for photos)
def get_photo_date(photo_path):
    try:
        img = Image.open(photo_path)
        exif = img._getexif()
        if exif:
            for tag, value in exif.items():
                if TAGS.get(tag) == "DateTimeOriginal":
                    return value.split()[0].replace(":", "-")  # Format YYYY-MM-DD
    except Exception as e:
        logging.warning(f"EXIF error for {photo_path}: {e}")

# Use file system date as fallback
    try:
        return datetime.fromtimestamp(os.path.getctime(photo_path)).strftime('%Y-%m-%d')
    except Exception as e:
        logging.warning(f"Timestamp error for {photo_path}: {e}") 
        return "0000-00-00" # Invalid Date 

# GET original creation date from video metadata using FFmpeg
def get_video_date(video_path):
    try:
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_entries", "format_tags=creation_time",
            video_path
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        metadata = json.loads(result.stdout)

        # Extract creation date
        creation_time = metadata.get("format", {}).get("tags", {}).get("creation_time")
        if creation_time:
            return creation_time.split("T")[0]  # Extract YYYY-MM-DD
    except Exception as e:
        logging.warning(f"ffprobe error for {video_path}: {e}")
    
    # Use file system date as fallback
    try:
        return datetime.fromtimestamp(os.path.getctime(video_path)).strftime('%Y-%m-%d')
    except Exception as e:
        logging.warning(f"Timestamp error for {video_path}: {e}")
        return "0000-00-00" # Invalid Date 

# If file = image
def is_photo(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith("image")

# If file = video
def is_video(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith("video")

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
def get_media_date(file_path):
    if is_photo(file_path):
        return get_photo_date(file_path)
    elif is_video(file_path):
        return get_video_date(file_path)
    return "0000-00-00"

def main() -> None:
    """
    Entry point of the script: sorts and moves photos/videos into year/month folders.
    """
# Process each file in the SOURCE_DIR
for file in os.listdir(SOURCE_DIR):
    file_path = os.path.join(SOURCE_DIR, file)

    if not os.path.isfile(file_path):
        continue  # Skip non-file items (directories, etc.)

    # Determine if the file is a photo or video and set the target directory (input your subfolder path if you want subfolders in both/either image or video target DIR. e.g. "raw")
    if is_photo(file_path):
        TARGET_DIR = IMAGE_TARGET_DIR
        subfolder = ""  # Photos go into the month folder
    elif is_video(file_path):
        TARGET_DIR = VIDEO_TARGET_DIR
        subfolder = ""  # Videos go into the month folder
    else:
        print(f"Skipping unsupported file type: {file}")
        continue 

    # Get the date for organizing
    date = get_media_date(file_path)

    # Validate date format
    if "-" not in date or len(date.split('-')) < 2:
        print(f"Skipping {file} due to invalid date: {date}")
        continue

    year, month = date.split('-')[:2]  # Extract YYYY and MM

    # Define year/month/subfolder paths
    year_folder = os.path.join(TARGET_DIR, year)
    month_folder = os.path.join(year_folder, month)
    final_folder = os.path.join(month_folder, subfolder) if subfolder else month_folder

    # Ensure directories exist
    os.makedirs(final_folder, exist_ok=True)

    # Generate unique filename if needed
    new_filename = get_unique_filename(final_folder, file)

    # Move file to the correct folder
    shutil.move(file_path, os.path.join(final_folder, new_filename))
    print(f"Moved {file} to {final_folder} as {new_filename}")
    
if __name__ == "__main__":
    main()

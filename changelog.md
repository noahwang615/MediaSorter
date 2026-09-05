# Changelog for MediaSorter

## [v2.0.2]
- Added `make_proof` service to the solution
- Able to toggle proof service upon installation
- Created a central install script to allow user to choose local or docker install
- Updated repo structure

## [v2.0.1]
- Added Docker deployment support:
    - `Dockerfile` (Python 3.11-slim + ffmpeg + Pillow/pillow-heif)
    - `docker-compose.yml` mounting photo/video source & destination folders as volumes
    - `entrypoint.sh` sleep-loop scheduler (`RUN_INTERVAL_SECONDS`, default hourly) \u2014 no external cron needed
    - `Makefile` with `build`/`up`/`down`/`restart`/`logs`/`status`/`clean` targets (macOS/Linux)
    - Interactive `install_scripts/install_docker.sh` and `install_scripts/install_docker.bat` to collect paths and generate `.env`
    - Changed local install scripts name to `install_local` from just generic `install`.
- `mediasorter.py` now reads `MEDIA_SRC`, `PHOTO_DEST`, `VIDEO_DEST` environment variables (falling back to the existing hardcoded defaults for non-Docker use)

## [v1.5] - 2026-06-04
- Added `Pillow-heif` dependency to requirements.txt
- Updated the install scripts to resolve project base path
- Added test dir for local testing before deploying to working environment
- Improved the main script logic
    - Refined HEIC parsing
    - Added dependency checks for `pillow-heif` and `ffprobe`
    - Improved logging, including log file output from the script
    - Clarified comments around function purpose and user-editable paths.

## [v1.0] - 2025-08-01
- Released on Github
- Basic media sorting by year/month folders implemented
- Duplicate file handling
- Create log file with info and warning levels
- Provided python dependency install scripts for Windows and Linux/macOS
- Created README with installation and usage instructions

## [Maybe for a future release]
- Include python and ffmpeg install snippet in `install.bat` and `install.sh` for their respective OS (at least just cover the basic Windows, MacOS, Debian, and Ubuntu)
- Perhaps if it's a popular demand, include porting photo with original px to a `/raw` folder and add photo proofing snippet to port all proofed photo to `/proof` inside their `yyyy/mm` directory
- Maybe I'll even think about adding a quick "Getting Started" video tutorial or something
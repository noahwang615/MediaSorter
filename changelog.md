# Changelog for MediaSorter

## [v1.5.0] - 2026-06-04
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
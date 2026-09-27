# MediaSorter

MediaSorter moves photos and videos from one folder into year/month folders based on their metadata. It supports common image formats, including HEIC/HEIF, and uses `ffprobe` to read video metadata.

MediaSorter moves files instead of copying them. Keep backups of your media before the first run.

## Features

- Sorts photos and videos into `YYYY/MM` folders.
- Creates destination folders automatically.
- Avoids overwriting duplicates by adding `_2`, `_3`, and so on.
- Writes logs to `logs/mediasorter.log` and the console.
- Can run once manually, on a schedule, or continuously in Docker.
- Optionally creates smaller JPEG proof images for sorted photos.

## Requirements

**For Docker:**

- Docker Engine and the Compose plugin, or Docker Desktop

**For a local installation:**
- Python 3.11 or newer
- FFmpeg, including the `ffprobe` command
- Git, if cloning the repository

The local installer installs the Python packages from `scripts/requirements.txt` (`Pillow`, `pillow-heif`, and `python-dotenv`). The Docker image includes Python, FFmpeg, and those packages.

## Installation

Run installation on the machine where MediaSorter will process the files. For a NAS or remote server, connect over SSH first and clone the repository there.

### 1. Get the project

```bash
git clone https://github.com/noahwang615/MediaSorter.git
cd MediaSorter
```

You can also download the repository as a ZIP file and open a terminal in the extracted folder.

### 2. Choose an installation mode

### Docker installation

On macOS or Linux:

```bash
./install.sh
```

Choose `1` when prompted. You can also run the Docker installer directly:

```bash
./docker_install/install_docker.sh
```

On Windows, run `install.bat` and choose Docker, or run `docker_install\install_docker.bat`.

The Docker installer prompts for:

- `MEDIA_SRC`: the host folder where new media is placed
- `PHOTO_DEST`: the host folder for sorted photos
- `VIDEO_DEST`: the host folder for sorted videos
- `RUN_INTERVAL_SECONDS`: how often the container checks the source folder
- Whether to enable the optional proof-generation service

It creates the selected folders, writes `.env`, and builds the `mediasorter:latest` image. Docker must be running before the installer builds the image.

### Running with Docker

The Docker entrypoint runs one sorting pass, waits for `RUN_INTERVAL_SECONDS` (default `3600`), and repeats. No external scheduler is required.

Using Make on macOS/Linux:

```bash
make up       # start in the background
make status   # show container status
make sort     # manually trigger a sort pass immediately
make logs     # follow logs
make restart  # restart after configuration changes
make down     # stop the container
make clean    # stop and remove the built image
```

Without Make, use Docker Compose directly:

```bash
docker compose up -d
docker compose ps
docker compose logs -f
docker compose down
```

### Manual triggers (Docker)

To run an immediate sorting or proofing pass on demand without waiting for the scheduled loop interval:

- **macOS / Linux (using Make):**
  ```bash
  make sort     # trigger media sorting pass
  make proof    # trigger proof image generation pass
  ```
- **Windows (Command Prompt / PowerShell):**
  Run the batch scripts located in the `manual_trigger/` folder:
  ```cmd
  manual_trigger\manual_sort_trigger.bat
  manual_trigger\manual_proof_trigger.bat
  ```
- **Direct Docker Compose command:**
  ```bash
  docker compose exec mediasorter python scripts/mediasorter.py
  ```

After changing `.env`, restart the stack so Compose reloads the values:

```bash
docker compose up -d
```

The container writes persistent logs to `logs/` in the project. The source and destination folders remain on the host and are mounted into the container.

### Local Python installation

On macOS or Linux:

```bash
./install.sh
```

Choose `2` when prompted. The local installer:

1. Checks for Python 3.11 or newer.
2. Upgrades `pip` and installs `scripts/requirements.txt`.
3. Checks that `ffprobe` is available.
4. Prompts for the source, photo destination, and video destination folders.
5. Creates those folders and writes the settings to `.env`.

On Windows, run `install.bat` and choose the local installation option. Python must be available as `python`, and `ffprobe` must be available in `PATH`.

### Running locally

After local installation, run one sorting pass from the project root:

```bash
python3 scripts/mediasorter.py
```

On Windows:

```text
python scripts\mediasorter.py
```

Put media in `MEDIA_SRC` before running the command. Sorted photos and videos are moved into `PHOTO_DEST/YYYY/MM` and `VIDEO_DEST/YYYY/MM`.

Local mode runs once and exits. To run it automatically, schedule the command with cron, Windows Task Scheduler, or your NAS scheduler. Use the full path to the Python executable and `scripts/mediasorter.py` in the scheduled task.

Example cron entry that runs hourly:

```cron
0 * * * * /usr/bin/python3 /path/to/MediaSorter/scripts/mediasorter.py
```

## Configuration

Both installation modes use a `.env` file in the project root. A local run loads this file directly. Docker Compose uses it to bind host folders into the container.

Example:

```dotenv
MEDIA_SRC=/path/to/mediadump
PHOTO_DEST=/path/to/photos
VIDEO_DEST=/path/to/videos
RUN_INTERVAL_SECONDS=3600
```

The default local paths, when these variables are not set, are:

```text
data/mediadump
data/photos
data/videos
```

Relative paths are resolved from the project root. `MEDIA_SRC`, `PHOTO_DEST`, and `VIDEO_DEST` should be host paths when running Docker. Do not commit `.env` if it contains private paths or other machine-specific settings.

## Proof images

Proof generation creates JPEG previews in a `proof` subfolder below each photo month folder. It is optional.

During Docker installation, answer `y` when asked to enable the proof service. Set `PROOF_INTERVAL_SECONDS` to control its interval; the default is `86400` seconds. Then start the stack normally:

```bash
make up
make proof-logs
```

To generate proofs once instead of enabling the service:

```bash
make proof
```

The one-shot command uses the configured `PHOTO_DEST` path from `.env`.

## Examples

Given this source folder:

```text
mediadump/
├── IMG_1234.HEIC
├── IMG_2345.mov
├── baby.png
└── birthday.mp4
```

MediaSorter produces paths like:

```text
photos/2022/02/raw/IMG_1234.HEIC
photos/2024/08/raw/baby.png
videos/2024/07/IMG_2345.mov
videos/2023/12/birthday.mp4
```

The exact year and month come from the media metadata. Files with duplicate names receive a numeric suffix instead of replacing an existing file.

## Troubleshooting

- **Python is not found:** install Python 3.11 or newer and ensure it is available as `python3` on macOS/Linux or `python` on Windows.
- **`ffprobe` is not found:** install FFmpeg and add its `bin` directory to `PATH`.
- **A file is skipped:** check the console output or `logs/mediasorter.log`. Files without usable dates or unsupported formats may be skipped.
- **Docker paths are wrong:** edit `MEDIA_SRC`, `PHOTO_DEST`, and `VIDEO_DEST` in `.env`, then run `docker compose up -d` again.

## Development

Install the development requirements and run the test suite with:

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m pytest -q
```

Useful Make targets include `make test`, `make test-mediasort`, `make test-makeproofs`, and `make test-docker`.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

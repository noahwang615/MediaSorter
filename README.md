# MediaSorter

This script automatically organizes your photos and videos into year/month folders by parsing creation dates from their metadata. Perfect for quickly offloading and tidying up your digital memories.

I would recommend setting this up as a cronjob or scheduled task (feel free to test it out manually before automating the job), and I recommend keeping the name "mediadump" for simplicity's sake.

The script performs a move function instead of copy, so your mediadump folder will be emptied once the operation is complete. As a scheduled job, it won't do anything if the mediadump folder is empty (no harm in having it run every day). 
So offload your photos and videos into mediadump, let the machine do the tedious work, and get on with your life.

# Table of Contents
### [What it does](#feature)

### [What you need](#req)

### [Installation](#ins)

### [How to configure paths](#conf)

### [How to run it](#use)

### [Automate](#bonus)

### [Docker Deployment](#docker)

### [Examples](#exp)

### [Logging](#log)

### [Contributing](#cont)

### [FAQ](#faq)

### [Credits & License](#cred)


## What it does?

- Moves photos and videos into folders by year and month (e.g., /photos/2024/08/)

- Works with lots of image and video formats (using Pillow and ffprobe)

- Won’t overwrite files — if duplicates exist, it adds _2, _3, etc.

- Creates folders for you as needed

- Logs helpful info and warnings so you can see what’s going on

## What you need <a name="req"></a>

- Python 3.11 or newer installed on your computer or remote machine

- Pillow Python package (for photo metadata)

- FFmpeg with ffprobe (for video metadata)

If you don’t have these already, the install script handles it for you.

## Installing on a NAS or Remote Host

If you plan to run MediaSorter on a NAS, home server, or another remote machine, you should install it on that remote system, not just on your local computer.

In practice, that usually means:

- Connect to the remote host over SSH.
- Clone this repository on that host.
- Run the Python setup and install script from that host.
- Configure your scheduled task or cron job there as well.
- This README does not cover SSH setup in detail, but if you want MediaSorter to run automatically on a remote machine, make sure you are connected to that machine before following the installation steps below.


## Installation <a name="ins"></a>

*Note: If you are installing this on a NAS or remote host, SSH into that system first and run the following commands there.*

### 1. Download the project:

``` bash
git clone https://github.com/noahwang615/MediaSorter.git
cd MediaSorter
```
Or download the project as zip by clicking on the **Code** dropdown and click **Download Zip**

### 2. Run the install script:

**On macOS/Linux**

Open a terminal, then run:

```bash
./install.sh
```

**On Windows:**

Open Command Prompt and run

```text
.\install.bat
```

**The install script will check for Python 3 installation and prompt if missing.**

- Upgrade pip and install Python dependencies from requirements.txt.

- Check for ffprobe (part of FFmpeg) and prompt to install it if necessary.

- After successful installation, you will be able to run this operation.

    - *If you need help with installing Python or ffmpeg* [Install Python](https://www.python.org/downloads/), [Install FFMpeg](https://ffmpeg.org/download.html)

    - *If you know how to work with cmd/terminal, or would rather work that cmd/terminals...just google it, Google AI summary does a pretty good job giving you the answers*

## How to configure paths <a name="conf"></a>

Edit the `mediasorter.py` script and update the default directories at the top of the script: (you can open and edit the `mediasorter.py` script by right-click and open with notepad or texteditor)

```python
########## USER EDIT PATHS BELOW - CHANGE THESE FOR YOUR SETUP ##########

# SOURCE_DIR_DEFAULT = os.path.join(PROJECT_BASE, "mediadump")  <-- Uncomment if using default path (mediadump folder in project root)
SOURCE_DIR_DEFAULT = "path/to/your/mediadump_directory"          # <-- Change this to your source path
IMAGE_TARGET_DIR_DEFAULT = "path/to/your/image_target_directory"  # <-- Change this to your desired image target path
VIDEO_TARGET_DIR_DEFAULT = "path/to/your/video_target_directory"  # <-- Change this to your desired video target path

"""
Here's an example how my path works. I store all my media in a Synology instance, so my Media_AutoSort is inside Synology looking for those directories
SOURCE_DIR_DEFAULT = "/volume1/homes/mediadump"
IMAGE_TARGET_DIR_DEFAULT = "/volume1/homes/images"
VIDEO_TARGET_DIR_DEFAULT = "/volume1/homes/video"
"""

SOURCE_DIR = os.environ.get("MEDIA_SRC", SOURCE_DIR_DEFAULT)
IMAGE_TARGET_DIR = os.environ.get("PHOTO_DEST", IMAGE_TARGET_DIR_DEFAULT)
VIDEO_TARGET_DIR = os.environ.get("VIDEO_DEST", VIDEO_TARGET_DIR_DEFAULT)

########## USER EDIT PATHS BELOW - CHANGE THESE FOR YOUR SETUP ##########
```

The `DEFAULT` values are used when running the script directly (no Docker). If the `MEDIA_SRC`, `PHOTO_DEST`, or `VIDEO_DEST` environment variables are set (as they are inside the Docker container — see [Docker Deployment](#docker)), they override the defaults.

*You can use absolute or relative paths. The script will create folders if they don’t exist.*

### Here's an example

```python
SOURCE_DIR_DEFAULT = "C:/noahwang/MediaSorter/mediadump" # path in my computer's local drive
IMAGE_TARGET_DIR_DEFAULT = "/volume1/homes/images" # path to my photo destination in network folder
VIDEO_TARGET_DIR_DEFAULT = "/volume1/homes/videos" # path to my video destination in network folder
```

## How to run it: <a name="use"></a>

**Usage Recommendation:** I would just set up a cronjob, scheduled tasks, or whatever automated job to just run this script periodically (mine runs every hour in my remote server). Nothing will happen if there's nothing in mediadump folder anyway. More hands-off, less manual steps. 

1. Put all your photos and videos in /mediadump

2. Open a terminal or command prompt inside the MediaSorter folder.

3. Run the script:

```bash
python scripts/mediasorter.py
```

## Automate to forget about it <a name="bonus"></a>
*Want this to run by itself regularly? Here’s how!*


### On Mac/Linux - Cron job
- Open the terminal and enter

```bash
crontab -e
```

- Add this line (change path if needed)

```bash
0 * * * * /usr/bin/python3 /path/to/your/mediasorter.py
```

*note: this cron runs the job for every hour, change the timing to your preference. If you don't know how to set up cron job, [Click here to learn how to schedule](https://crontab.guru/)*

### On Windows - Task Scheduler: 

Open Task Scheduler

Click “Create Basic Task...”

Choose your schedule (daily, hourly, etc.)

For “Action,” pick “Start a Program”

In “Program/script” put your Python path, e.g.:
`C:\Users\YourName\AppData\Local\Programs\Python\Python39\python.exe`
*make sure you replace the placeholder "YourName" with what's in your actual path*

In “Add arguments,” put the full path to mediasorter.py, e.g.:
`C:\path\to\MediaSorter\mediasorter.py`

Save and enjoy automatic sorting

*note: If your python is not located in the usual spot and you don't remember where you installed it, run ```where python``` in your command line*

## Docker Deployment <a name="docker"></a>

Prefer not to install Python, Pillow, or ffmpeg yourself? Run MediaSorter as a Docker container instead — all dependencies are baked into the image, and the container re-runs the sort job on a timer (default: hourly) so you don't need cron or Task Scheduler.

**Requirements:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Mac/Windows) or Docker Engine + the Compose plugin (Linux/NAS), able to run `docker compose`.

### 1. Run the interactive Docker install script

**On macOS/Linux**

```bash
./docker_install/install_docker.sh
```

**On Windows**

```text
.\docker_install\install_docker.bat
```

You'll be prompted for:

- **Media dump source folder** — where you drop raw photos/videos (host path, mounted as `MEDIA_SRC`)
- **Photo destination folder** — sorted photos land here as `yyyy/mm/` (mounted as `PHOTO_DEST`)
- **Video destination folder** — sorted videos land here as `yyyy/mm/` (mounted as `VIDEO_DEST`)
- **Run interval in seconds** — how often the container re-scans the source folder (default `3600`)

This writes a `.env` file at the project root and builds the `mediasorter:latest` image via `docker compose build`. Re-running the script reuses your previous answers as defaults.

### 2. Start/stop the container

On macOS/Linux, a `Makefile` wraps the common `docker compose` commands:

```bash
make up       # start the container in the background
make logs     # follow logs
make status   # show container status
make down     # stop the container
make restart  # down + up
make clean    # stop and remove the built image
```

On Windows (or anywhere without `make`), use `docker compose` directly:

```text
docker compose up -d
docker compose logs -f
docker compose down
```

### How it works

- The image is built from `docker_install/Dockerfile` (Python 3.11-slim + ffmpeg + Pillow/pillow-heif).
- `docker-compose.yml` mounts your three host folders into the container at fixed internal paths, plus `./logs` for persistent log output on the host.
- `entrypoint.sh` loops: run `mediasorter.py`, sleep `RUN_INTERVAL_SECONDS`, repeat — acting as a built-in scheduler so no external cron is required.
- To change paths or the interval later, edit `.env` directly (or re-run the install script) and `docker compose up -d` again to pick up the change.

### For Synology DSM (what I use): 
- Open Control Panel > Task Scheduler > Create Scheduled Task
- Input the name, and modify the script's schedule
- Enter ```/usr/bin/python /path/to/mediasorter.py``` under User-Defined script


## Examples <a name="exp"></a>

Suppose your source directory contains these files:

```text
/mediadump
    IMG_1234.HEIC
    IMG_2345.mov
    baby.png
    birthday.mp4
```
**After running the script, the files will be sorted into:**

```text
/your/photo_directory/2022/02/IMG_1234.HEIC
/your/photo_directory/2024/08/baby.png
/your/video_directory/2024/07/IMG_2345.mov
/your/video_directory/2023/12/birthday.mp4
```
**If a file with the same name exists in the target folder, the script will save the new file as filename_2.ext, filename_3.ext, etc.**

## Logging <a name="log"></a>

The script uses Python's logging module. By default, you'll see info and warning messages in the console. You can set a different log level inside the script (e.g., DEBUG, INFO, WARNING, ERROR).
*(e.g., Change the `logging.basicConfig(level=logging.INFO)` line inside mediasorter.py).*

## Contributing <a name="cont"></a>

Fork the repo, make tweaks you like, and open a pull request if you want to share your improvements!


## FAQ <a name="faq"></a>
**Q: Why does the script skip some files?**

A:
- The script skips files it can't read dates from or unsupported formats. Check the terminal logs when you run it for clues.
- You may also want to make sure you have `pip`, `Pillow`, and `FFmpeg` installed., make sure **[Installation](#ins)** step is done before running this operation

**Q: How do I use this with network drives or cloud folders?**

A: Yep! Set `MEDIA_SRC`, `PHOTO_DEST`, and `VIDEO_DEST` in `.env` to your network or cloud folder paths.

**Q: What file types are supported?**

A: Common photo types like JPG, PNG, HEIC, and video types like MP4, MOV, and more that Pillow and ffprobe handle.

## Credits <a name="cred"></a>
Thanks to my excessively organized wife for insisting on our family photos being sorted and thus inspiring me to make this tool. We're both happy now that it gets done and I don't have to do it manually. 

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

---

## Happy Sorting!
Drop your media in, hit run, and relax while your files get cleaned up.


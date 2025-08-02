# MediaSorter

This script automatically organize your photos and videos into year/month folders by parsing creation dates from their metadata. Perfect for quickly offloading and tidying up your digital memories.

I would recommend setting this up as cronjob or scheduled task (feel free to test it out manually before automating the job), and I would recommend keeping the name "mediadump" for simplicity sake.
The script does perform a move function instead of copy, so your mediadump folder will be emptied once the operation is complete
So as a scheduled job, it wouldn't do anything if the mediadump folder is empty anyway. So just make it easy for yourself, dump all your stuff into mediadump, and let the machine do the tedious work in seconds and get on with your lives.

# Table of Contents
### [Features](#feature)

### [Requirements](req)

### [Installation](ins)

### [Configuration](conf)

### [Usage](usage)

### [Bonus: set it up for automation](bonus)

### [Examples](exp)

### [Logging](log)

### [Contributing](cont)

### [FAQ](faq)

### [License](lic)


## Features <a name="feature"></a>
* Sorts media into folders by year and month

* Handles both photos (EXIF) and videos (ffprobe metadata)

* Duplicate-safe: Won't overwrite files, generates unique names if needed

* Automatically creates folders as required

* Logs actions and warnings for easy troubleshooting

## Requirements <a name="req"></a>

Install Python 3.8+ on the machine that is going to be running the script (local or remote server)

* Pillow: for image EXIF data handling

* FFmpeg (ffprobe): for video metadata extraction

## Installation <a name="ins"></a>

### 1. Clone the repository:

``` bash
git clone https://github.com/noahwang615/MediaSorter.git
cd MediaSorter
```
Or download the project as zip

### 2. Run the provided install script for your platform to set up dependencies:

**On macOS/Linux**

Open a terminal, then run:

```bash
bash ./install_scripts/install.sh
On Windows:
```

**Open Command Prompt and run**

```text
.\install_scripts\install.bat
```

The install script will check for Python 3 installation and prompt if missing.

Upgrade pip and install Python dependencies from requirements.txt.

Check for ffprobe (part of FFmpeg) and prompt to install it if necessary.

After successful installation, you can run the script as usual:

```bash
python media_sort.py
```

## Configuration <a name="conf"></a>

Edit the media_sorter.py script and update the directories at the top:

```python
SOURCE_DIR = "path/to/your/mediadump"
IMAGE_TARGET_DIR = "path/to/your/photos"
VIDEO_TARGET_DIR = "path/to/your/videos"
```
You can use absolute or relative paths. The script will create folders if they don’t exist.

## Usage: <a name="usage"></a>

**Usage Recommendation:** I would just set up a cronjob, scheduled tasks, or whatever automated job to just run this script periodically (mine runs every hour in my remote server). Nothing will happen if there's nothing in mediadump folder anyway. More hands-off, less manual steps. 

* You connect your phone to do offload your photos and videos

* You put all your media in /mediadump

* If you set it up via cron or scheduled tasks, then you're done

* If you opted for manual trigger, you can simply run the script from your terminal:

```bash
python media_sort.py
```

## Bonus: set it up for automation <a name="bonus"></a>
*(For those that don't know how to set up automations in your systems)*


### For cron:
- Open your terminal
- crontab -e
- 0 * * * * /usr/bin/python3 /path/to/your/media_sort.py

note: that cron is setup for every hour, feel free to change the frequency. If you don't know how to set up cron job, [Click here to learn how to schedule](https://crontab.guru/)

### For Windows Task Scheduler: 
- Launch Task Scheduler
- In the Action pane, click Create Basic Tasks
- Fill in the names and stuff, I would recommend choosing "Run whether user is logged in or not"
- Click Trigger and click new, do whatever interval you want
- Go to the Action tab, Action = Start a Program, Program/Script = "C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python<VersionNumber>\python.exe", Add arguments = "path/to/media_sorter.py"

*note: If your python is not located in the usual spot and you don't remember where you installed it, run where python in your command line*

### For Synology DSM (what I use): 
- Open Control Panel > Task Scheduler > Create Scheduled Task
- Input the name, and modify the script's schedule
- Enter python3 /path/to/media_sorter.py under User-Defined script


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
/your/photo_directory/2024/07/IMG_1234.HEIC
/your/photo_directory/2024/07/baby.png
/your/video_directory/2024/07/IMG_2345.mov
/your/video_directory/2023/12/birthday.mp4
```
**If a file with the same name exists in the target folder, the script will save the new file as filename_2.ext, filename_3.ext, etc.**

## Logging <a name="log"></a>

The script uses Python's logging module. By default, you'll see info and warning messages in the console. You can set a different log level inside the script (e.g., DEBUG, INFO, WARNING, ERROR).

## Contributing <a name="cont"></a>

Feel free to contribute

Fork the repository

Create a new branch:
git checkout -b feature/your-feature

Do your thing and make it better if you want

## FAQ <a name="faq"></a>
**Q: Why does the script skip some files?**
A: Check the log output for warnings. Skipped files are usually unsupported types or missing date information in their metadata. 

**Q: How do I use this with network drives or cloud folders?**
A: Just set the SOURCE_DIR, IMAGE_TARGET_DIR, and VIDEO_TARGET_DIR to the paths. I personally just have the folder in my network drive so the path can be as simple as it can be, and I can set a cron job in the network drive to have it go on its own.

**Q: What file types are supported?**
A: All standard image and video file types recognized by their MIME type and by the Pillow/ffprobe tools.


## License <a name="lic"></a>

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

Happy Sorting!

# MediaSorter

This script automatically organizes your photos and videos into year/month folders by parsing creation dates from their metadata. Perfect for quickly offloading and tidying up your digital memories.

I would recommend setting this up as a cronjob or scheduled task (feel free to test it out manually before automating the job), and I recommend keeping the name "mediadump" for simplicity's sake.

The script performs a move function instead of copy, so your mediadump folder will be emptied once the operation is complete. As a scheduled job, it won't do anything if the mediadump folder is empty (no harm in having it run every day). 
So offload your photos and videos into mediadump, let the machine do the tedious work, and get on with your life.

# Table of Contents
### [What’s it do](#feature)

### [What you need](#req)

### [Installation](#ins)

### [How to configure paths](#conf)

### [How to run it](#use)

### [Automate](#bonus)

### [Examples](#exp)

### [Logging](#log)

### [Contributing](#cont)

### [FAQ](#faq)

### [Credits & License](#cred)


## What’s it do?

- Moves photos and videos into folders by year and month (e.g., /photos/2024/08/)

- Works with lots of image and video formats (using Pillow and ffprobe)

- Won’t overwrite files — if duplicates exist, it adds _2, _3, etc.

- Creates folders for you as needed

- Logs helpful info and warnings so you can see what’s going on

## What you need <a name="req"></a>

- Python 3.8 or newer installed on your computer

- Pillow Python package (for photo metadata)

- FFmpeg with ffprobe (for video metadata)

If you don’t have these already, the install script handles it for you.

## Installation <a name="ins"></a>

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
bash ./install_scripts/install.sh
```

**On Windows:**

Open Command Prompt and run

```text
.\install_scripts\install.bat
```

The install script will check for Python 3 installation and prompt if missing.

Upgrade pip and install Python dependencies from requirements.txt.

Check for ffprobe (part of FFmpeg) and prompt to install it if necessary.

After successful installation, you will be able to run this operation.

*If you need help with installing Python or ffmpeg* [Install Python](https://www.python.org/downloads/), [Install FFMpeg](https://ffmpeg.org/download.html)

*If you know how to work with cmd/terminal, or would rather work that cmd/terminals...just google it, Google AI summary does a pretty good job giving you the answers*

## How to configure paths <a name="conf"></a>

Edit the mediasorter.py script and update the directories at the top of the script: (you can open and edit the `mediasorter.py` script by right-click and open with notepad or texteditor)

```python
SOURCE_DIR = "(path to MediaSorter folder)/mediadump"
IMAGE_TARGET_DIR = "path/to/your/photos"
VIDEO_TARGET_DIR = "path/to/your/videos"
```
Please replace these placeholder path with your actual path
*You can use absolute or relative paths. The script will create folders if they don’t exist.*

### Here's my example

```python
SOURCE_DIR = "C:/noahwang/MediaSorter/mediadump" # path in my computer's local drive
IMAGE_TARGET_DIR = "/volume1/homes/images" # path to my photo destination in network folder
VIDEO_TARGET_DIR = "/volume1/homes/videos" # path to my video destination in network folder
```

## How to run it: <a name="use"></a>

**Usage Recommendation:** I would just set up a cronjob, scheduled tasks, or whatever automated job to just run this script periodically (mine runs every hour in my remote server). Nothing will happen if there's nothing in mediadump folder anyway. More hands-off, less manual steps. 

1. Put all your photos and videos in /mediadump

2. Open a terminal or command prompt inside the MediaSorter folder.

3. Run the script:

```bash
python mediasorter.py
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

### For Synology DSM (what I use): 
- Open Control Panel > Task Scheduler > Create Scheduled Task
- Input the name, and modify the script's schedule
- Enter ```python3 /path/to/mediasorter.py``` under User-Defined script


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

A: Yep! Just set `SOURCE_DIR`, `IMAGE_TARGET_DIR`, and `VIDEO_TARGET_DIR` to your network or cloud folder paths.

**Q: What file types are supported?**

A: Common photo types like JPG, PNG, HEIC, and video types like MP4, MOV, and more that Pillow and ffprobe handle.

## Credits <a name="cred"></a>
Thanks to my excessively organized wife for insisting on our family photos being sorted and thus inspiring me to make this tool. We're both happy now that it gets done and I don't have to do it manually. 

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

---

## Happy Sorting!
Drop your media in, hit run, and relax while your files get cleaned up.


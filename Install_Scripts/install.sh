#!/bin/bash

# Check for Python3
if ! command -v python3 &> /dev/null
then
    echo "Python3 could not be found, please install Python3 first."
    exit
fi

# Install dependencies
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt

# Check for ffprobe
if ! command -v ffprobe &> /dev/null
then
    echo "ffprobe (part of ffmpeg) is not installed. Please install ffmpeg."
    exit
fi

echo "Installation completed!"

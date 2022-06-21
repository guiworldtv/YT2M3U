#!/bin/bash
python3 -m pip install requests

python3 YouTubeLinkGrabber.py > ./youtubestaticvideo.m3u

echo M3U grabbed.

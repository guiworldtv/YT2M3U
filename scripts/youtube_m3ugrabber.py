#! /usr/bin/python3

banner = r'''
###########################################################################
#                                  >> https://github.com/guiworldtv       #
###########################################################################


'''

import requests
import os

def grab(url):
    response = requests.get(url, timeout=15).text
    if '.m3u8' not in response:
        with open("temp.txt", "w") as f:
            response = requests.get(url).text
            f.write(response)
        with open("temp.txt", "r") as f:
            response = f.read()
            if '.m3u8' not in response:
                print('https://raw.githubusercontent.com/guiworldtv/MEU-IPTV-FULL/main/VideoOFFAirYT.m3u8')
                return
    end = response.find('.m3u8') + 5
    tuner = 100
    while True:
        if 'https://' in response[end-tuner : end]:
            link = response[end-tuner : end]
            start = link.find('https://')
            end = link.find('.m3u8') + 5
            break
        else:
            tuner += 5
    print(f"{link[start : end]}")

print('#EXTM3U x-tvg-url="https://iptv-org.github.io/epg/guides/ar/mi.tv.epg.xml"')
print('#EXTM3U x-tvg-url="https://github.com/botallen/epg/releases/download/latest/epg.xml"')

class Channel:
    def __init__(self, ch_name, grp_title, tvg_logo, tvg_id):
        self.ch_name = ch_name
        self.grp_title = grp_title
        self.tvg_logo = tvg_logo
        self.tvg_id = tvg_id

    def __str__(self):
        return f'\n#EXTINF:-1 group-title="{self.grp_title}" tvg-logo="{self.tvg_logo}" tvg-id="{self.tvg_id}", {self.ch_name}'

channels = []

with open('../youtube_channel_info.txt', errors="ignore") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('~~'):
            continue
        if not line.startswith('https:'):
            line = line.split('|')
            ch_name = line[0].strip()
            grp_title = line[1].strip().title()
            tvg_logo = line[2].strip()
            tvg_id = line[3].strip()
            channels.append(Channel(ch_name, grp_title, tvg_logo, tvg_id))
        else:
            grab(line)

for channel in channels:
    print(channel)

if os.path.exists("temp.txt"):
    os.remove("temp.txt")
    os.remove("watch*")

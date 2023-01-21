#! /usr/bin/python3

import os
import sys
import m3u8
import logging
import requests

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

banner = r'''
###########################################################################
#                                  >> https://github.com/guiworldtv       #
###########################################################################

'''

def is_windows():
    return 'win' in sys.platform

def grab_m3u8_link(url):
    try:
        response = requests.get(url, timeout=15).text
        m3u8_obj = m3u8.loads(response)
        return m3u8_obj.playlists[0].uri
    except m3u8.exceptions.M3U8Error as e:
        logger.error(f'Error parsing M3U8: {e}')
        return 'https://raw.githubusercontent.com/guiworldtv/MEU-IPTV-FULL/main/VideoOFFAirYT.m3u8'
    except requests.exceptions.RequestException as e:
        logger.error(f'Error while trying to get the link: {e}')
        return 'https://raw.githubusercontent.com/guiworldtv/MEU-IPTV-FULL/main/VideoOFFAirYT.m3u8'

def main():
    print(banner)
    print('#EXTM3U x-tvg-url="https://iptv-org.github.io/epg/guides/ar/mi.tv.epg.xml"')
    print('#EXTM3U x-tvg-url="https://github.com/botallen/epg/releases/download/latest/epg.xml"')
    
    with open('../youtube_channel_info.txt', 'r', errors="ignore") as f:
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
                print(f'\n#EXTINF:-1 group-title="{grp_title}" tvg-logo="{tvg_logo}" tvg-id="{tvg_id}", {ch_name}')
            else:
                link = grab_m3u8_link(line)
                print(link)
    if is_windows():
        logger.info('Windows OS detected, skipping temp file deletion')
    else:
        if 'temp.txt' in os.listdir():
            os.system('rm temp.txt')
            os.system('rm watch*')

if __name__ == '__main__':
    main()

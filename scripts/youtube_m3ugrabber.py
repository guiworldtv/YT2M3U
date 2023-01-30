#! /usr/bin/python3

# Uma string raw que será exibida como banner
banner = r'''
###########################################################################
#                                  >> https://github.com/guiworldtv       #
###########################################################################
'''

import requests
import os
import sys

# Variável que indica se o sistema é Windows
windows = False

# Verifica se o sistema é Windows pelo nome da plataforma
if 'win' in sys.platform:
    windows = True

def grab(url):
    # Busca o conteúdo da URL
    response = requests.get(url, timeout=15).text
    
    # Verifica se o conteúdo possui o link '.m3u8'
    if '.m3u8' not in response:
        # Busca o conteúdo novamente
        response = requests.get(url).text
        
        # Verifica se o conteúdo agora possui o link '.m3u8'
        if '.m3u8' not in response:
            # Se o sistema é Windows, exibe uma mensagem de erro
            if windows:
                print('https://raw.githubusercontent.com/guiworldtv/MEU-IPTV-FULL/main/VideoOFFAirYT.m3u8')
                return
            # Usa o comando wget para baixar o conteúdo da URL
            os.system(f'wget {url} -O temp.txt')
            response = ''.join(open('temp.txt').readlines())
            
            # Verifica se o conteúdo baixado possui o link '.m3u8'
            if '.m3u8' not in response:
                print('https://raw.githubusercontent.com/guiworldtv/MEU-IPTV-FULL/main/VideoOFFAirYT.m3u8')
                return
    # Encontra a posição do final da string '.m3u8'
    end = response.find('.m3u8') + 5
    tuner = 100
    while True:
        # Verifica se a string '.m3u8' é precedida por 'https://'
        if 'https://' in response[end-tuner : end]:
            # Armazena a string que começa com 'https://' e termina com '.m3u8'
            link = response[end-tuner : end]
            start = link.find('https://')
            end = link.find('.m3u8') + 5
            break
        else:
            tuner += 5
    # Exibe o link encontrado
    print(f"{link[start : end]}")

# Imprime as informações de cabeçalho M3U
print('#EXTM3U x-tvg-url="https://iptv-org.github.io/epg/guides/ar/mi.tv.epg.xml"')
print('#EXTM3U x-tvg-url="https://github.com/botallen/epg/releases/download/latest/epg.xml"')
print(banner)
#s = requests.Session()
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
            print(f'\n#EXTINF:-1 group-title="{grp_title}" tvg-logo="{tvg_logo}" tvg-id="{tvg_id}", {ch_name}')
        else:
            grab(line)
            
if 'temp.txt' in os.listdir():
    os.system('rm temp.txt')
    os.system('rm watch*')

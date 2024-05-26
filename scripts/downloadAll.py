#!/usr/bin/env python
# encoding: utf-8

import os
import json
import time
import codecs
import requests
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}


def downloadSetCardList(cardListUrl, error_list):
    rs = list()
    r, soup = None, None
    try:
        r = requests.get(cardListUrl, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
    except Exception as e:
        error_list.append('{"type": "index", "info": "%s"}' % cardListUrl)
        return rs

    if soup is not None:
        for tr in soup.find_all('tr'):
            attrs = tr.attrs
            try:
                if "data-hover" in attrs and attrs["data-hover"] is not None:
                    img_url = attrs["data-hover"].replace("_XS.png", ".png")
                    pos = img_url.rfind('/')
                    img_filename = img_url[pos+1:]
                    rs.append({"img_url": img_url, "img_filename": img_filename})
            except Exception as e:
                error_list.append('{"type": "index_record", "info": "%s"}' % cardListUrl)
    return rs


def download2File(url, dirpath, filename):
    print(url)
    filepath = os.path.join(dirpath, filename)
    print(filepath)
    with requests.get(url, stream=True, headers=headers, timeout=60) as r:
        r.raise_for_status()
        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk:
                f.write(chunk)
    print('#' * 100)
    return filepath


def downloadImagesByCardList(cardList, output_dirpath, error_list):
    for card in cardList:
        try:
            download2File(card['img_url'], output_dirpath, card['img_filename'])
        except Exception as e:
            error_list.append('{"type": "downloadImagesByCardList", "info": "%s"}' % card['img_url'])
        time.sleep(0.5)


def downloadOneSet(config):
    error_list = list()

    setId = config['SetId']
    os.system("mkdir -p %s" % setId)
    os.system("mkdir -p %s/img" % setId)

    cardList = downloadSetCardList("https://limitlesstcg.com/cards/%s?show=all&display=list" % setId, error_list)
    with codecs.open("%s/card_list.txt" % setId, mode='w', encoding='utf-8') as fp:
        for card in cardList:
            fp.write(card['img_filename'] + "\t" + card['img_url'])
            fp.write('\n')

    downloadImagesByCardList(cardList, "./%s/img" % setId, error_list)

    with codecs.open("%s/error_list.txt" % setId, mode='w', encoding='utf-8') as fp:
        for line in error_list:
            fp.write(line)
            fp.write('\n')


downloadedSets = [
{
    "SetId": "SUM",
    "SetName": "Sun & Moon",
    "CardSize": 172
},
{
    "SetId": "GRI",
    "SetName": "Guardians Rising",
    "SeriesName": "Sun & Moon",
    "CardSize": 169
},
{
    "SetId": "BUS",
    "SetName": "Burning Shadows",
    "SeriesName": "Sun & Moon",
    "CardSize": 169
},
{
    "SetId": "CIN",
    "SetName": "Crimson Invasion",
    "SeriesName": "Sun & Moon",
    "CardSize": 124
},
{
    "SetId": "UPR",
    "SetName": "Ultra Prism",
    "SeriesName": "Sun & Moon",
    "CardSize": 173
},
{
    "SetId": "CES",
    "SetName": "Celestial Storm",
    "SeriesName": "Sun & Moon",
    "CardSize": 183
},
{
    "SetId": "LOT",
    "SetName": "Lost Thunder",
    "SeriesName": "Sun & Moon",
    "CardSize": 236
},
{
    "SetId": "TEU",
    "SetName": "Team Up",
    "SeriesName": "Sun & Moon",
    "CardSize": 205
},
{
    "SetId": "UNB",
    "SetName": "Unbroken Bonds",
    "SeriesName": "Sun & Moon",
    "CardSize": 234
},
{
    "SetId": "UNM",
    "SetName": "Unified Minds",
    "SeriesName": "Sun & Moon",
    "CardSize": 258
},
]

toBeDownloadSets = [
{
    "SetId": "FLI",
    "SetName": "Forbidden Light",
    "SeriesName": "Sun & Moon",
    "CardSize": 146
},
{
    "SetId": "CEC",
    "SetName": "Cosmic Eclipse",
    "SeriesName": "Sun & Moon",
    "CardSize": 271
},
]


if __name__ == "__main__":
    for setConfig in toBeDownloadSets:
        downloadOneSet(setConfig)



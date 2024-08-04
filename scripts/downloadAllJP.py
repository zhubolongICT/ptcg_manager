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

    cardList = downloadSetCardList("https://limitlesstcg.com/cards/jp/%s?show=all&display=list" % setId, error_list)
    with codecs.open("%s/card_list.txt" % setId, mode='w', encoding='utf-8') as fp:
        for card in cardList:
            fp.write(card['img_filename'] + "\t" + card['img_url'])
            fp.write('\n')

    downloadImagesByCardList(cardList, "./%s/img" % setId, error_list)

    with codecs.open("%s/error_list.txt" % setId, mode='w', encoding='utf-8') as fp:
        for line in error_list:
            fp.write(line)
            fp.write('\n')


toBeDownloadSets = [
{
    "SetId": "SJ",
    "SetName": "Special Deck Set: Zacian & Zamazenta vs Eternatus",
    "SeriesName": "Sword & Shield",
    "CardSize": 30
},
{
    "SetId": "S8a",
    "SetName": "25th Anniversary Collection",
    "SeriesName": "Sword & Shield",
    "CardSize": 37
},
{
    "SetId": "S8",
    "SetName": "Fusion Arts",
    "SeriesName": "Sword & Shield",
    "CardSize": 115
},
{
    "SetId": "SP5",
    "SetName": "V-UNION Special Card Sets",
    "SeriesName": "Sword & Shield",
    "CardSize": 13
},
{
    "SetId": "S7D",
    "SetName": "Skyscraping Perfection",
    "SeriesName": "Sword & Shield",
    "CardSize": 79
},
{
    "SetId": "S7R",
    "SetName": "Blue Sky Stream",
    "SeriesName": "Sword & Shield",
    "CardSize": 79
},
{
    "SetId": "SH",
    "SetName": "Family Pokémon Card Game",
    "SeriesName": "Sword & Shield",
    "CardSize": 59
},
{
    "SetId": "S6a",
    "SetName": "Eevee Heroes",
    "SeriesName": "Sword & Shield",
    "CardSize": 87
},
{
    "SetId": "SGG",
    "SetName": "High-Class Deck Gengar VMAX",
    "SeriesName": "Sword & Shield",
    "CardSize": 20
},
{
    "SetId": "SGI",
    "SetName": "High-Class Deck Inteleon VMAX",
    "SeriesName": "Sword & Shield",
    "CardSize": 23
},
{
    "SetId": "SP4",
    "SetName": "VMAX Special Set Eevee Heroes",
    "SeriesName": "Sword & Shield",
    "CardSize": 8
},
{
    "SetId": "S6H",
    "SetName": "Silver Lance",
    "SeriesName": "Sword & Shield",
    "CardSize": 83
},
{
    "SetId": "S6K",
    "SetName": "Jet-Black Spirit",
    "SeriesName": "Sword & Shield",
    "CardSize": 83
},
{
    "SetId": "SP3",
    "SetName": "Jumbo-Pack Set Silver Lance & Jet-Black Spirit",
    "SeriesName": "Sword & Shield",
    "CardSize": 6
},
{
    "SetId": "S5a",
    "SetName": "Matchless Fighters",
    "SeriesName": "Sword & Shield",
    "CardSize": 84
},
{
    "SetId": "S5I",
    "SetName": "Single Strike Master",
    "SeriesName": "Sword & Shield",
    "CardSize": 81
},
{
    "SetId": "S5R",
    "SetName": "Rapid Strike Master",
    "SeriesName": "Sword & Shield",
    "CardSize": 81
},
{
    "SetId": "SF",
    "SetName": "Premium Trainer Box Single Strike & Rapid Strike",
    "SeriesName": "Sword & Shield",
    "CardSize": 33
},
{
    "SetId": "SC2",
    "SetName": "Charizard VMAX Starter Set 2",
    "SeriesName": "Sword & Shield",
    "CardSize": 21
},
{
    "SetId": "SEF",
    "SetName": "Venusaur VMAX Starter Set",
    "SeriesName": "Sword & Shield",
    "CardSize": 21
},
{
    "SetId": "SEK",
    "SetName": "Blastoise VMAX Starter Set",
    "SeriesName": "Sword & Shield",
    "CardSize": 20
},
{
    "SetId": "S4a",
    "SetName": "Shiny Star V",
    "SeriesName": "Sword & Shield",
    "CardSize": 326
},
{
    "SetId": "SP2",
    "SetName": "VMAX Special Set",
    "SeriesName": "Sword & Shield",
    "CardSize": 8
},
{
    "SetId": "S4",
    "SetName": "Amazing Volt Tackle",
    "SeriesName": "Sword & Shield",
    "CardSize": 111
},
{
    "SetId": "S3a",
    "SetName": "Legendary Heartbeat",
    "SeriesName": "Sword & Shield",
    "CardSize": 85
},
{
    "SetId": "SD",
    "SetName": "V Starter Decks",
    "SeriesName": "Sword & Shield",
    "CardSize": 127
},
{
    "SetId": "S3",
    "SetName": "Infinity Zone",
    "SeriesName": "Sword & Shield",
    "CardSize": 110
},
{
    "SetId": "S2a",
    "SetName": "Explosive Walker",
    "SeriesName": "Sword & Shield",
    "CardSize": 78
},
{
    "SetId": "SCd",
    "SetName": "Grimmsnarl VMAX Starter Set",
    "SeriesName": "Sword & Shield",
    "CardSize": 20
},
{
    "SetId": "SCr",
    "SetName": "Charizard VMAX Starter Set",
    "SeriesName": "Sword & Shield",
    "CardSize": 21
},
{
    "SetId": "S2",
    "SetName": "Rebel Clash",
    "SeriesName": "Sword & Shield",
    "CardSize": 106
},
{
    "SetId": "S1a",
    "SetName": "VMAX Rising",
    "SeriesName": "Sword & Shield",
    "CardSize": 78
},
{
    "SetId": "SP1",
    "SetName": "Zacian & Zamazenta Box",
    "SeriesName": "Sword & Shield",
    "CardSize": 7
},
{
    "SetId": "S1H",
    "SetName": "Shield",
    "SeriesName": "Sword & Shield",
    "CardSize": 68
},
{
    "SetId": "S1W",
    "SetName": "Sword",
    "SeriesName": "Sword & Shield",
    "CardSize": 68
},
{
    "SetId": "SB",
    "SetName": "Premium Trainer Box Sword & Shield",
    "SeriesName": "Sword & Shield",
    "CardSize": 24
},
{
    "SetId": "SAf",
    "SetName": "Starter Set V Fighting",
    "SeriesName": "Sword & Shield",
    "CardSize": 25
},
{
    "SetId": "SAg",
    "SetName": "Starter Set V Grass",
    "SeriesName": "Sword & Shield",
    "CardSize": 24
},
{
    "SetId": "SAl",
    "SetName": "Starter Set V Lightning",
    "SeriesName": "Sword & Shield",
    "CardSize": 25
},
{
    "SetId": "SAr",
    "SetName": "Starter Set V Fire",
    "SeriesName": "Sword & Shield",
    "CardSize": 24
},
{
    "SetId": "SAw",
    "SetName": "Starter Set V Water",
    "SeriesName": "Sword & Shield",
    "CardSize": 24
},
{
    "SetId": "SP",
    "SetName": "Sword & Shield Promotional Cards",
    "SeriesName": "Sword & Shield",
    "CardSize": 300
},
{
    "SetId": "SM12a",
    "SetName": "Tag All Stars",
    "SeriesName": "Sun & Moon",
    "CardSize": 173
},
{
    "SetId": "SM12",
    "SetName": "Alter Genesis",
    "SeriesName": "Sun & Moon",
    "CardSize": 95
},
{
    "SetId": "SM11b",
    "SetName": "Dream League",
    "SeriesName": "Sun & Moon",
    "CardSize": 68
},
{
    "SetId": "SM11a",
    "SetName": "Remix Bout",
    "SeriesName": "Sun & Moon",
    "CardSize": 73
},
{
    "SetId": "SM11",
    "SetName": "Miracle Twin",
    "SeriesName": "Sun & Moon",
    "CardSize": 106
},
{
    "SetId": "SMM",
    "SetName": "Tag Team GX Starter Sets",
    "SeriesName": "Sun & Moon",
    "CardSize": 31
},
{
    "SetId": "SM10b",
    "SetName": "Sky Legend",
    "SeriesName": "Sun & Moon",
    "CardSize": 62
},
{
    "SetId": "SMP2",
    "SetName": "Movie Special Pack Great Detective Pikachu",
    "SeriesName": "Sun & Moon",
    "CardSize": 25
},
{
    "SetId": "SM10a",
    "SetName": "GG End",
    "SeriesName": "Sun & Moon",
    "CardSize": 62
},
{
    "SetId": "SML",
    "SetName": "Family Pokémon Card Game",
    "SeriesName": "Sun & Moon",
    "CardSize": 51
},
{
    "SetId": "SM10",
    "SetName": "Double Blaze",
    "SeriesName": "Sun & Moon",
    "CardSize": 107
},
{
    "SetId": "SMN",
    "SetName": "Tag Team GX Deck Build Box",
    "SeriesName": "Sun & Moon",
    "CardSize": 29
},
{
    "SetId": "SM9b",
    "SetName": "Full Metal Force",
    "SeriesName": "Sun & Moon",
    "CardSize": 62
},
{
    "SetId": "SMK",
    "SetName": "Brock & Misty Trainer Battle Decks",
    "SeriesName": "Sun & Moon",
    "CardSize": 31
},
{
    "SetId": "SM9a",
    "SetName": "Night Unison",
    "SeriesName": "Sun & Moon",
    "CardSize": 63
},
{
    "SetId": "SM9",
    "SetName": "Tag Bolt",
    "SeriesName": "Sun & Moon",
    "CardSize": 109
},
{
    "SetId": "SMJ",
    "SetName": "Tag Team GX Premium Trainer Box",
    "SeriesName": "Sun & Moon",
    "CardSize": 35
},
{
    "SetId": "SMI",
    "SetName": "Starter Sets Flareon & Jolteon & Vaporeon",
    "SeriesName": "Sun & Moon",
    "CardSize": 38
},
{
    "SetId": "SM8b",
    "SetName": "GX Ultra Shiny",
    "SeriesName": "Sun & Moon",
    "CardSize": 243
},
{
    "SetId": "SM8a",
    "SetName": "Dark Order",
    "SeriesName": "Sun & Moon",
    "CardSize": 58
},
{
    "SetId": "SM8",
    "SetName": "Super Burst Impact",
    "SeriesName": "Sun & Moon",
    "CardSize": 103
},
{
    "SetId": "SM7b",
    "SetName": "Fairy Rise",
    "SeriesName": "Sun & Moon",
    "CardSize": 56
},
{
    "SetId": "SMH",
    "SetName": "GX Starter Decks",
    "SeriesName": "Sun & Moon",
    "CardSize": 131
},
{
    "SetId": "SM7a",
    "SetName": "Thunderclap Spark",
    "SeriesName": "Sun & Moon",
    "CardSize": 66
},
{
    "SetId": "SM7",
    "SetName": "Charisma of the Ripped Sky",
    "SeriesName": "Sun & Moon",
    "CardSize": 104
},
{
    "SetId": "SM6b",
    "SetName": "Champion's Road",
    "SeriesName": "Sun & Moon",
    "CardSize": 77
},
{
    "SetId": "SM6a",
    "SetName": "Dragon Storm",
    "SeriesName": "Sun & Moon",
    "CardSize": 59
},
{
    "SetId": "SM6",
    "SetName": "Forbidden Light",
    "SeriesName": "Sun & Moon",
    "CardSize": 102
},
{
    "SetId": "SMG",
    "SetName": "Ultra Sun & Ultra Moon Deck Battle Box",
    "SeriesName": "Sun & Moon",
    "CardSize": 12
},
{
    "SetId": "SM5p",
    "SetName": "Ultra Force",
    "SeriesName": "Sun & Moon",
    "CardSize": 56
},
{
    "SetId": "SM5M",
    "SetName": "Ultra Moon",
    "SeriesName": "Sun & Moon",
    "CardSize": 72
},
{
    "SetId": "SM5S",
    "SetName": "Ultra Sun",
    "SeriesName": "Sun & Moon",
    "CardSize": 72
},
{
    "SetId": "SMF",
    "SetName": "Premium Trainer Box Ultra Sun & Ultra Moon",
    "SeriesName": "Sun & Moon",
    "CardSize": 12
},
{
    "SetId": "SME",
    "SetName": "Starter Set Solgaleo-GX & Lunala-GX",
    "SeriesName": "Sun & Moon",
    "CardSize": 21
},
{
    "SetId": "SM4p",
    "SetName": "GX Battle Boost",
    "SeriesName": "Sun & Moon",
    "CardSize": 120
},
{
    "SetId": "SM4A",
    "SetName": "Beasts from the Ultradimension",
    "SeriesName": "Sun & Moon",
    "CardSize": 55
},
{
    "SetId": "SM4S",
    "SetName": "Awakened Heroes",
    "SeriesName": "Sun & Moon",
    "CardSize": 55
},
{
    "SetId": "SM3p",
    "SetName": "Shining Legends",
    "SeriesName": "Sun & Moon",
    "CardSize": 77
},
{
    "SetId": "SM3H",
    "SetName": "Did You See The Fighting Rainbow",
    "SeriesName": "Sun & Moon",
    "CardSize": 57
},
{
    "SetId": "SM3N",
    "SetName": "Light Consuming Darkness",
    "SeriesName": "Sun & Moon",
    "CardSize": 57
},
{
    "SetId": "SM2p",
    "SetName": "Let's Face New Trials",
    "SeriesName": "Sun & Moon",
    "CardSize": 61
},
{
    "SetId": "SMD",
    "SetName": "Ash VS Team Rocket Half Decks",
    "SeriesName": "Sun & Moon",
    "CardSize": 30
},
{
    "SetId": "SM2K",
    "SetName": "Islands Await You",
    "SeriesName": "Sun & Moon",
    "CardSize": 55
},
{
    "SetId": "SM2L",
    "SetName": "Alolan Moonlight",
    "SeriesName": "Sun & Moon",
    "CardSize": 55
},
{
    "SetId": "SMC",
    "SetName": "Starter Set Tapu Bulu-GX",
    "SeriesName": "Sun & Moon",
    "CardSize": 21
},
{
    "SetId": "SM1p",
    "SetName": "Sun and Moon plus",
    "SeriesName": "Sun & Moon",
    "CardSize": 63
},
{
    "SetId": "SMP1",
    "SetName": "Rockruff Full Strength Deck",
    "SeriesName": "Sun & Moon",
    "CardSize": 13
},
{
    "SetId": "SM1M",
    "SetName": "Collection Moon",
    "SeriesName": "Sun & Moon",
    "CardSize": 66
},
{
    "SetId": "SM1S",
    "SetName": "Collection Sun",
    "SeriesName": "Sun & Moon",
    "CardSize": 66
},
{
    "SetId": "SMA",
    "SetName": "Starter Set SM",
    "SeriesName": "Sun & Moon",
    "CardSize": 68
},
{
    "SetId": "SMB",
    "SetName": "Premium Trainer Box",
    "SeriesName": "Sun & Moon",
    "CardSize": 15
},
{
    "SetId": "SM0",
    "SetName": "Pikachu and new Friends",
    "SeriesName": "Sun & Moon",
    "CardSize": 4
},
{
    "SetId": "SMP",
    "SetName": "Sun and Moon Promotional Cards",
    "SeriesName": "Sun & Moon",
    "CardSize": 440
}
]

#------------------------------------------------------------------------------------------------

hasBeenDownloadedSets = [
{
    "SetId": "S12a",
    "SetName": "VSTAR Universe",
    "SeriesName": "Sword & Shield",
    "CardSize": 172
},
{
    "SetId": "SO",
    "SetName": "Special Deck Set: Charizard VSTAR vs Rayquaza VMAX",
    "SeriesName": "Sword & Shield",
    "CardSize": 32
},
{
    "SetId": "S12",
    "SetName": "Paradigm Trigger",
    "SeriesName": "Sword & Shield",
    "CardSize": 114
},
{
    "SetId": "S11a",
    "SetName": "Incandescent Arcana",
    "SeriesName": "Sword & Shield",
    "CardSize": 85
},
{
    "SetId": "SP6",
    "SetName": "VSTAR Special Set",
    "SeriesName": "Sword & Shield",
    "CardSize": 6
},
{
    "SetId": "S11",
    "SetName": "Lost Abyss",
    "SeriesName": "Sword & Shield",
    "CardSize": 116
},
{
    "SetId": "SPD",
    "SetName": "VSTAR&VMAX High-Class Deck Deoxys",
    "SeriesName": "Sword & Shield",
    "CardSize": 21
},
{
    "SetId": "SPZ",
    "SetName": "VSTAR&VMAX High-Class Deck Zeraora",
    "SeriesName": "Sword & Shield",
    "CardSize": 21
},
{
    "SetId": "S10b",
    "SetName": "Pokémon GO",
    "SeriesName": "Sword & Shield",
    "CardSize": 91
},
{
    "SetId": "S10a",
    "SetName": "Dark Phantasma",
    "SeriesName": "Sword & Shield",
    "CardSize": 89
},
{
    "SetId": "S10D",
    "SetName": "Time Gazer",
    "SeriesName": "Sword & Shield",
    "CardSize": 79
},
{
    "SetId": "S10P",
    "SetName": "Space Juggler",
    "SeriesName": "Sword & Shield",
    "CardSize": 79
},
{
    "SetId": "S9a",
    "SetName": "Battle Region",
    "SeriesName": "Sword & Shield",
    "CardSize": 84
},
{
    "SetId": "SLD",
    "SetName": "Starter Set Darkrai VSTAR",
    "SeriesName": "Sword & Shield",
    "CardSize": 20
},
{
    "SetId": "SLL",
    "SetName": "Starter Set Lucario VSTAR",
    "SeriesName": "Sword & Shield",
    "CardSize": 21
},
{
    "SetId": "S9",
    "SetName": "Star Birth",
    "SeriesName": "Sword & Shield",
    "CardSize": 116
},
{
    "SetId": "SI",
    "SetName": "Starter Decks 100",
    "SeriesName": "Sword & Shield",
    "CardSize": 427
},
{
    "SetId": "S8b",
    "SetName": "VMAX Climax",
    "SeriesName": "Sword & Shield",
    "CardSize": 277
},

]

##################################################################################################


if __name__ == "__main__":
    for setConfig in toBeDownloadSets:
        downloadOneSet(setConfig)



import os
import codecs
import json
import requests

from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}


def generate_empty_zhs_en_mapping(img_dirpath, index_filepath):
    jobj = {}
    zhs_en_dict = generate_zhs_en_dict()
    for filename in os.listdir(img_dirpath):
        if filename.endswith('png') or filename.endswith('jpg'):
            filepath = os.path.join(img_dirpath, filename)
            l_p = filename.find('-')
            r_p = filename.rfind('.')
            card_zhs_name = filename[l_p+1:r_p]
            if card_zhs_name not in jobj:
                jobj[card_zhs_name] = list()
            # jobj[card_zhs_name].append(filepath)
            if card_zhs_name in zhs_en_dict:
                jobj[card_zhs_name] = {"name": zhs_en_dict[card_zhs_name]['en'], "en_cards": [], "zhs_cards": []}
            else:
                jobj[card_zhs_name] = {"name": "", "en_cards": [], "zhs_cards": []}
    with codecs.open(index_filepath, mode='w', encoding='utf-8') as fp:
        fp.write(json.dumps(jobj, default=lambda obj: obj.__dict__, 
            sort_keys=True, ensure_ascii=False, indent=4))


def generate_zhs_en_dict():
    r = requests.get("https://bulbapedia.bulbagarden.net/wiki/List_of_Chinese_Pok%C3%A9mon_names", headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    zhs_name_mapping = dict()

    for tr in soup.find_all('tr'):
        idx = 0
        attrs = list()
        for td in tr.find_all('td'):
            attrs.append(td.text.rstrip('\r\n'))
            
        if len(attrs) == 8:
            en_name = attrs[2]
            zht_name = attrs[3]
            zhs_name = attrs[4]
            
            if len(en_name) > 0 and len(zhs_name) > 0:
                zhs_name_mapping[zhs_name] = {"en": en_name, "zht": zht_name}

    return zhs_name_mapping


def load_zhs_mapping(mapping_filepath):
    jobj = None
    with codecs.open(mapping_filepath, mode='r', encoding='utf-8') as fp:
        jobj = json.load(fp)
    return jobj


def convert_zhsdeck_to_standard_deck(input_filepath, output_filepath, mapping_filepath):
    _type = None
    ofp = codecs.open(output_filepath, mode='w', encoding='utf-8')
    mappings = load_zhs_mapping(mapping_filepath)

    with codecs.open(input_filepath, mode='r', encoding='utf-8') as fp:
        for line in fp.readlines():
            line = line.rstrip('\r\n')
            if line.startswith('Pokémon'):
                _type = 'Pokémon'
                ofp.write(line)
            elif line.startswith('Trainer'):
                _type = 'Trainer'
                ofp.write(line)
            elif line.startswith('Energy'):
                _type = 'Energy'
                ofp.write(line)
            else:
                if len(line) > 0:
                    first_space_pos = line.find(' ')
                    _size = int(line[:first_space_pos])
                    zhs_name = line[first_space_pos+1:]
                    try:
                        if zhs_name in mappings:
                            set_id = mappings[zhs_name]["en_cards"][0]
                            ofp.write("%d %s %s" % (_size, zhs_name, set_id.replace("_", " ")))
                        else:
                            print("%s => can not found %s in mappings" % (input_filepath, zhs_name))
                    except:
                        print("%s has not cards" % zhs_name)
            ofp.write('\n')
    ofp.close()


def main():
    # generate_empty_zhs_en_mapping(img_dirpath='D://gao/ptcg/card_database/简中低清晰度',
    #     index_filepath='../index/zhs_cardbase_001.json')

    convert_zhsdeck_to_standard_deck(input_filepath='../deck/zhs/雷丘鸣鸣.txt',
        output_filepath='../deck/standard/雷丘鸣鸣.txt',
        mapping_filepath='../index/zhs_cardbase.json')


if __name__ == '__main__':
    main()


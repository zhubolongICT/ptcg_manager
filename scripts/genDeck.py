import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import os
import codecs
import json

from nine_grid_pinjie import process_nine_grid_pinjie


class Card(object):
    def __init__(self, _set, _id, _name, _type, _size):
        self.set = _set
        self.id = _id
        self.name = _name
        self.type = _type
        self.size = _size


def parse_standard_deck_text(filepath):
    _type = None
    card_list = list()
    with codecs.open(filepath, mode='r', encoding='utf-8') as fp:
        for line in fp.readlines():
            line = line.rstrip('\r\n')
            if line.startswith('Pokémon'):
                _type = 'Pokémon'
            elif line.startswith('Trainer'):
                _type = 'Trainer'
            elif line.startswith('Energy'):
                _type = 'Energy'
            else:
                if len(line) > 0:
                    first_space_pos = line.find(' ')
                    last_space_pos = line.rfind(' ')
                    _size = int(line[:first_space_pos])
                    _id = line[last_space_pos+1:]
                    p = line[:last_space_pos].rfind(' ')
                    _set = line[p+1:last_space_pos]
                    _name = line[first_space_pos+1:last_space_pos-4]
                    card_list.append(Card(_set, _id, _name, _type, _size))
    return card_list


def batch_process_standard_deck():
    DECK_DIRPATH = "../deck/tobe_gen"
    OUTPUT_DIRPATH = "../deck/img"

    for filename in os.listdir(DECK_DIRPATH):
        if not filename.endswith(".txt"):
            continue
        filepath = os.path.join(DECK_DIRPATH, filename)
        card_list = parse_standard_deck_text(filepath)
        image_filepathes = list()
        for card in card_list:
            # print(json.dumps(card, default=lambda obj: obj.__dict__, 
            #     sort_keys=True, ensure_ascii=False))
            _set = card.set
            _id = card.id
            try:
                _id = '%03d' % int(card.id)
            except:
                pass

            if _set.startswith("csm"):
                # 中文环境
                for i in range(card.size):
                    image_filepathes.append("../card_database/zhs/%s_%s.png" % (_set, _id))
            elif _set == 'tmp':
                for i in range(card.size):
                    image_filepathes.append("../card_database/tmp/%s.png" % (_id))
            else:
                for i in range(card.size):
                    image_filepathes.append("../card_database/en/%s/img/%s_%s_R_EN.png" % (
                        _set, _set, _id))

    
        process_nine_grid_pinjie(image_filepathes, OUTPUT_DIRPATH, filename[:-4], True)


def main():
    batch_process_standard_deck()


if __name__ == "__main__":
    main()

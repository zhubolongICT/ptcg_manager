import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
import os
import json
import codecs


SAVE_AS_JPG = True


def process_deck_view(image_filepath_and_cnt_list, output_image_dirpath, setId):
    w = 736                      # 每张小图片的宽度
    h = 1024                     # 每张小图片的高度
    IMAGE_ROW = 4                # 合成后图片一共有几行小图片
    IMAGE_COLUMN = 8             # 合成后图片一共有几列小图片

    # 通过留白将每张卡牌调整为 66mm * 91mm 的卡套
    delta_w = 25
    pinjie_w = (w + delta_w) * IMAGE_COLUMN

    delta_h = 51
    pinjie_h = (h + delta_h) * IMAGE_ROW

    # pinjie_w / pinjie_h => 297 / 210  A4纸尺寸
    
    # output_image_dirpath 合成后图片的存储目录 （可能有多张，每张一共 ROW*COLUMN 个小图片）
     
    # 定义图像拼接函数
    def image_compose(input_image_filepath_and_cnt_list, output_image_filepath):
        to_image = Image.new(mode='RGBA', size=(pinjie_w, pinjie_h), color=(255, 255, 255)) #创建一个新图
        # 循环遍历，把每张图片按顺序粘贴到对应位置上
        dh = int(delta_h/2)
        for y in range(1, IMAGE_ROW + 1):
            dw = int(delta_w/2)
            for x in range(1, IMAGE_COLUMN + 1):
                if (IMAGE_COLUMN * (y - 1) + x - 1) < len(input_image_filepath_and_cnt_list):
                    image_filepath, image_cnt = (
                        input_image_filepath_and_cnt_list[IMAGE_COLUMN * (y - 1) + x - 1][0],
                        input_image_filepath_and_cnt_list[IMAGE_COLUMN * (y - 1) + x - 1][1])
                    from_image = Image.open(image_filepath).resize((w, h), Image.ANTIALIAS)

                    # TODO: write cnt number
                    to_image.paste(from_image, ((x - 1) * (w+delta_w) + dw, (y - 1) * (h+delta_h) + dh))
        

        image_cnt_list = list()
        for el in input_image_filepath_and_cnt_list:
            image_cnt_list.append(el[1])

        draw = ImageDraw.Draw(to_image)
        for i in range(IMAGE_ROW):
            for j in range(IMAGE_COLUMN):
                if len(image_cnt_list) <= 0:
                    break
                _cnt = image_cnt_list.pop(0)
                
                # if _cnt <= 1:
                #     continue
                
                b = 100
                x = (j * (w+delta_w) + int((w+delta_w)/2) - delta_w)
                y = (i * (h+delta_h) + int(h+delta_h-b))
                draw.rectangle((x, y, x+b, y+b), fill=(0, 0, 255), outline=(255, 255, 255))

                font = ImageFont.truetype(r'../fonts/msyhbd.ttf', 80)
                
                draw.text((x+int(b/4), y), text="%d" % _cnt, font=font, align ="left") 
            if len(image_cnt_list) <= 0:
                break


        if SAVE_AS_JPG:
            new_to_image = to_image.convert('RGB')
            new_to_image.save(output_image_filepath.replace('.png', '.jpg'), 
                format='JPEG', subsampling=0, quality=100)
        else:
            to_image.save(output_image_filepath) # 保存新图


    batch_size = IMAGE_ROW * IMAGE_COLUMN
    index = 0
    cnt = 0
    while index < len(image_filepath_and_cnt_list):
        cnt += 1
        output_image_filepath = os.path.join(output_image_dirpath, "%s_%03d.png" % (setId, cnt))
        image_compose(image_filepath_and_cnt_list[index : index+batch_size], output_image_filepath)
        index += batch_size


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
                    _set = line[last_space_pos-3:last_space_pos]
                    _name = line[first_space_pos+1:last_space_pos-4]
                    card_list.append(Card(_set, _id, _name, _type, _size))
    return card_list


def batch_process_standard_deckview():
    DECK_DIRPATH = "../deck/standard"
    OUTPUT_DIRPATH = "../deck/view"

    for filename in os.listdir(DECK_DIRPATH):
        if not filename.endswith(".txt"):
            continue
        filepath = os.path.join(DECK_DIRPATH, filename)
        card_list = parse_standard_deck_text(filepath)
        image_filepath_and_cnt_list = list()
        for card in card_list:
            # print(json.dumps(card, default=lambda obj: obj.__dict__, 
            #     sort_keys=True, ensure_ascii=False))
            _set = card.set
            _id = card.id
            try:
                _id = '%03d' % int(card.id)
            except:
                pass
            image_filepath_and_cnt_list.append(("../card_database/Sun & Moon/%s/img/%s_%s_R_EN.png" % (
                _set, _set, _id), card.size))

        process_deck_view(image_filepath_and_cnt_list, OUTPUT_DIRPATH, filename[:-4])


# def drawNumber():
#     im = Image.new('RGB', (500, 300), (128, 128, 128))
#     draw = ImageDraw.Draw(im)


#     draw.ellipse((100, 100, 150, 200), fill=(255, 0, 0), outline=(0, 0, 0))
#     draw.rectangle((200, 100, 300, 200), fill=(0, 192, 192), outline=(255, 255, 255))
#     draw.line((350, 200, 450, 100), fill=(255, 255, 0), width=10)

#     im.show()


if __name__ == "__main__":
    batch_process_standard_deckview()

    # drawNumber()

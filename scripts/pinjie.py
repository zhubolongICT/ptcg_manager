import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import os


w = 736                      # 每张小图片的宽度
h = 1024                     # 每张小图片的高度
IMAGE_ROW = 2                # 合成后图片一共有几行小图片
IMAGE_COLUMN = 4             # 合成后图片一共有几列小图片

# 通过留白将每张卡牌调整为 66mm * 91mm 的卡套
delta_w = 120
pinjie_w = w*4 + delta_w*4

delta_h = 186
pinjie_h = h*2 + delta_h*2

# pinjie_w / pinjie_h => 297 / 210  A4纸尺寸


def process(input_image_dirpath, output_image_dirpath, setId):

    # input_image_dirpath 输入图片集地址
    # output_image_dirpath 合成后图片的存储目录 （可能有多张，每张一共 ROW*COLUMN 个小图片）

    # 获取全部小图片的路径地址
    image_filepathes = list()
    for image_filename in os.listdir(input_image_dirpath):
        image_filepathes.append(os.path.join(input_image_dirpath, image_filename))
     
    # 定义图像拼接函数
    def image_compose(input_image_filepathes, output_image_filepath):
        to_image = Image.new('RGBA', (pinjie_w, pinjie_h)) #创建一个新图
        # 循环遍历，把每张图片按顺序粘贴到对应位置上
        dh = int(delta_h/2)
        for y in range(1, IMAGE_ROW + 1):
            dw = int(delta_w/2)
            for x in range(1, IMAGE_COLUMN + 1):
                if (IMAGE_COLUMN * (y - 1) + x - 1) < len(input_image_filepathes):
                    print(input_image_filepathes[IMAGE_COLUMN * (y - 1) + x - 1])
                    from_image = Image.open(input_image_filepathes[IMAGE_COLUMN * (y - 1) + x - 1]).resize(
                        (w, h), Image.ANTIALIAS)
                    to_image.paste(from_image, ((x - 1) * (w+delta_w) + dw, (y - 1) * (h+delta_h) + dh))
        
        draw = ImageDraw.Draw(to_image)

        # 画横线
        dw, dh = int(delta_w/2), int(delta_h/2)
        line_width=3
        draw.line(((0, dh), (pinjie_w, dh)), fill=(0, 0, 0), width=line_width)
        draw.line(((0, dh + h), (pinjie_w, dh + h)), fill=(0, 0, 0), width=line_width)
        draw.line(((0, delta_h + h + dh), (pinjie_w, delta_h + h + dh)), fill=(0, 0, 0), width=line_width)
        draw.line(((0, delta_h + 2*h + dh), (pinjie_w, delta_h + 2*h + dh)), fill=(0, 0, 0), width=line_width)

        # 画竖线
        draw.line(((dw, 0), (dw, pinjie_h)), fill=(0, 0, 0), width=line_width)
        draw.line(((dw+w, 0), (dw+w, pinjie_h)), fill=(0, 0, 0), width=line_width)
        draw.line(((dw+w+delta_w, 0), (dw+w+delta_w, pinjie_h)), fill=(0, 0, 0), width=line_width)
        draw.line(((dw+2*w+delta_w, 0), (dw+2*w+delta_w, pinjie_h)), fill=(0, 0, 0), width=line_width)
        draw.line(((dw+2*w+2*delta_w, 0), (dw+2*w+2*delta_w, pinjie_h)), fill=(0, 0, 0), width=line_width)
        draw.line(((dw+3*w+2*delta_w, 0), (dw+3*w+2*delta_w, pinjie_h)), fill=(0, 0, 0), width=line_width)
        draw.line(((dw+3*w+3*delta_w, 0), (dw+3*w+3*delta_w, pinjie_h)), fill=(0, 0, 0), width=line_width)
        draw.line(((dw+4*w+3*delta_w, 0), (dw+4*w+3*delta_w, pinjie_h)), fill=(0, 0, 0), width=line_width)

        to_image.save(output_image_filepath) # 保存新图


    batch_size = IMAGE_ROW * IMAGE_COLUMN
    index = 0
    cnt = 0
    while index < len(image_filepathes):
        cnt += 1
        output_image_filepath = os.path.join(output_image_dirpath, "%s_%03d.png" % (setId, cnt))
        image_compose(image_filepathes[index : index+batch_size], output_image_filepath)
        index += batch_size


def main():
    # DIR_PATH = '../card_database/Sun & Moon'
    # OUPUT_PINJIE_DIRPATH = '../pinjie'
    
    # process(input_image_dirpath=os.path.join(DIR_PATH, 'DET/img'), 
    #     output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='DET')

    # process(input_image_dirpath=os.path.join(DIR_PATH, 'DRM/img'), 
    #     output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='DRM')

    # process(input_image_dirpath=os.path.join(DIR_PATH, 'HIF/img'), 
    #     output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='HIF')

    # process(input_image_dirpath=os.path.join(DIR_PATH, 'SLG/img'), 
    #     output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='SLG')

    # process(input_image_dirpath=os.path.join(DIR_PATH, 'SMP/img'), 
    #     output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='SMP')


    # process(input_image_dirpath=os.path.join(DIR_PATH, 'BUS/img'), 
    #     output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='BUS')

    # process(input_image_dirpath=os.path.join(DIR_PATH, 'CEC/img'), 
    #     output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='CEC')
    
    # process(input_image_dirpath=os.path.join(DIR_PATH, 'CES/img'), 
    #     output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='CES')
    
    # process(input_image_dirpath=os.path.join(DIR_PATH, 'CIN/img'), 
    #     output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='CIN')
    
    # process(input_image_dirpath=os.path.join(DIR_PATH, 'FLI/img'), 
    #     output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='FLI')
    
    # process(input_image_dirpath=os.path.join(DIR_PATH, 'GRI/img'), 
    #     output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='GRI')

    # process(input_image_dirpath=os.path.join(DIR_PATH, 'LOT/img'), 
    #     output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='LOT')

    # process(input_image_dirpath=os.path.join(DIR_PATH, 'SUM/img'), 
    #     output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='SUM')

    # process(input_image_dirpath=os.path.join(DIR_PATH, 'TEU/img'), 
    #     output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='TEU')

    # process(input_image_dirpath=os.path.join(DIR_PATH, 'UNB/img'), 
    #     output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='UNB')

    # process(input_image_dirpath=os.path.join(DIR_PATH, 'UNM/img'), 
    #     output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='UNM')

    # process(input_image_dirpath=os.path.join(DIR_PATH, 'UPR/img'), 
    #     output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='UPR') 

    DIR_PATH = 'C:\\Users\\Administrator\\Downloads\\xxx'
    OUPUT_PINJIE_DIRPATH = '../pinjie'
    process(input_image_dirpath=os.path.join(DIR_PATH, 'temp/img'), 
            output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='temp') 


if __name__ == "__main__":
    main()

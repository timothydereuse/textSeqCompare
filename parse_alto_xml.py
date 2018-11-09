import xml.etree.ElementTree as ET
import textSeqCompare as tsc
import PIL as pil
import numpy as np
from PIL import Image, ImageDraw, ImageFont

fname = 'einsiedeln_001r'

tra_align, ocr_align = tsc.process(fname)

tree = ET.parse('./txt/' + fname + '_text.xml')

lt = list(tree.iter())

tlines = [x for x in lt if x.tag[-8:] == 'TextLine']
text_els = []

for line in tlines:
    text_els += list(line)

im = Image.open('./png/' + fname + '_text.png')
text_size = 40
fnt = ImageFont.truetype('./arial.ttf', text_size)
draw = ImageDraw.Draw(im)
for text in text_els:
    att = text.attrib
    dims = [att['HPOS'], att['VPOS'], att['WIDTH'], att['HEIGHT']]
    dims = [int(x) for x in dims]
    # dims[0] += 80

    shuf = np.random.randint(-8,8)
    box = [dims[0], dims[1] + shuf, dims[2] + dims[0], dims[3] + dims[1]]
    draw.rectangle(box, outline=0, width=5)
    draw.text((dims[0], dims[1] - text_size), att['CONTENT'], font=fnt, fill=0)
im.save('testimg.png')

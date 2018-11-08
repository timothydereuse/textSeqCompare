import xml.etree.ElementTree as ET
import textSeqCompare as tsc
import PIL as pil

fname = 'einsiedeln_001v'

tra_align, ocr_align = tsc.process(fname)

tree = ET.parse('./txt/' + fname + '_text.xml')

lt = list(tree.iter())

tlines = [x for x in lt if x.tag[-8:] == 'TextLine']
text_els = []

for line in tlines:
    text_els += list(line)

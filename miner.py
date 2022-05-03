from io import StringIO
import pdfplumber
from decimal import Decimal
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.converter import PDFPageAggregator
import glob
import os


def miner(in_file) -> 'plain text':
    all_miner_bbox = []
    parser = PDFParser(in_file)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = PDFPageAggregator(rsrcmgr, laparams=LAParams(line_overlap=0.5, char_margin=2.0,
                                                          line_margin=0.5, word_margin=0.1, boxes_flow=0.5,
                                                          detect_vertical=False, all_texts=False))
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    all_text = ''
    for page in PDFPage.create_pages(doc):
        miner_bbox = []
        interpreter.process_page(page)
        layout = device.get_result()
        page_width = layout.bbox[2]
        page_height = layout.bbox[3]
        for obj in layout._objs:
            if isinstance(obj, LTTextBox):
                # text = o.get_text()
                # bbox = list(o.bbox)
                for o in obj._objs:
                    if isinstance(o, LTTextLine):
                        text = o.get_text()
                        all_text += text
                        bbox = list(o.bbox)
                        bbox[0] = Decimal(str(bbox[0]))
                        bbox[1] = Decimal(str(abs(bbox[1] - page_height)))
                        bbox[2] = Decimal(str(bbox[2]))
                        bbox[3] = Decimal(str(abs(bbox[3] - page_height)))
                        assert bbox[1] < page_height and bbox[3] < page_height, "y coord of bbox out of range"
                        miner_bbox.append(bbox)
        all_miner_bbox.append(miner_bbox)
    return all_text, all_miner_bbox


# pdfplumber for visualization
def plumber(plum_file) -> 'list of pages as images':
    pdf = pdfplumber.open(plum_file)
    all_image = []
    for i, val in enumerate(pdf.pages):
        image = val.to_image(resolution=300)
        all_image.append(image)
    return all_image


in_file_loc = 'others/dummyy'
out_file_loc = ''
file = open(in_file_loc, 'rb')
plain_text, all_bbox = miner(file)
# with open('claim.txt', 'w') as f:
#     f.write(plain_text)
images = plumber(in_file_loc)
assert len(images) == len(all_bbox), "all_bbox and images should be equal"
for pos, img in enumerate(images):
    img.draw_rects(all_bbox[pos])
    img.save(f"{pos}.pdf")
    break





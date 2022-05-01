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
    parser = PDFParser(in_file)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = PDFPageAggregator(rsrcmgr, laparams=LAParams(line_overlap=0.5, char_margin=2.0,
                                                          line_margin=0.5, word_margin=0.1, boxes_flow=0.5,
                                                          detect_vertical=False, all_texts=False))
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    all_text = ''
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)
        layout = device.get_result()
        page_width = layout.bbox[2]
        page_height = layout.bbox[3]
        for obj in layout._objs:
            if isinstance(obj, LTTextBox):
                for o in obj._objs:
                    if isinstance(o, LTTextLine):
                        text = o.get_text()
                        all_text += text
    return all_text


in_file_loc = 'others/claim.pdf'
out_file_loc = ''
file = open(in_file_loc, 'rb')
plain_text = miner(file)
with open('claim.txt', 'w') as f:
    f.write(plain_text)





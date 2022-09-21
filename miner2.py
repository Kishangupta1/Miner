from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

import glob
in_path = "check"  # i/p dir
out_path = "check"  # o/p dir
import os

for files in glob.glob(in_path + '/*.pdf'):
    print(f'\nparsing file: {files}')
    file = files.split("\\")[-1]
    file = file.split(".")[0]
    inp = in_path + "/" + file
    out = out_path + "/" + file

    output_string = StringIO()

    for i in range(2):
        with open(inp + '.pdf', 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams(line_overlap = 0.5, char_margin = 2.0,
                                line_margin  = 0.5, word_margin  = 0.1, boxes_flow = 0.5,
                                detect_vertical = False, all_texts  = False))
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)

        with open(out + ".txt", "wb") as f:
            f.write(output_string.getvalue().encode())
            f.close()
        # print(output_string.getvalue())


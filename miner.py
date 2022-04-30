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


# output_string = StringIO()
all_bbox = []
with open('foo.pdf', 'rb') as in_file:
    parser = PDFParser(in_file)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = PDFPageAggregator(rsrcmgr, laparams=LAParams(line_overlap=0.5, char_margin=2.0,
                                                          line_margin=0.5, word_margin=0.1, boxes_flow=0.5,
                                                          detect_vertical=False, all_texts=False))
    interpreter = PDFPageInterpreter(rsrcmgr, device)
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
                        bbox = list(o.bbox)
                        bbox[0] = Decimal(str(bbox[0]))
                        bbox[1] = Decimal(str(abs(bbox[1]-page_height)))
                        bbox[2] = Decimal(str(bbox[2]))
                        bbox[3] = Decimal(str(abs(bbox[3]-page_height)))
                        assert bbox[1] < page_height and bbox[3] < page_height, "y coord of bbox out of range"
                        all_bbox.append(bbox)
                        # break
                        # print(text)
                        # if text.strip():
                        #     for c in o._objs:
                        #         if isinstance(layout.LTChar):
                        #             print(c.fontname)
                                    # "fontname %s" % c.fontname
                # if it's a container, recurse
            # elif isinstance(obj, pdfminer.layout.LTFigure):
            #     parse_obj(obj._objs)
            # else:
            #     pass
            # print(output_string.getvalue())

    # pdfplumber for visualization
    pdf = pdfplumber.open(in_file)
    for pos, val in enumerate(pdf.pages):
        image = val.to_image(resolution=300)
        image.draw_rects(all_bbox)
        image.save(f'a1.pdf')







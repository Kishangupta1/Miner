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

def miner(in_file) -> 'list of line_text bbox of pages':
    all_miner_bbox = []
    parser = PDFParser(in_file)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = PDFPageAggregator(rsrcmgr, laparams=LAParams(line_overlap=0.5, char_margin=2.0,
                                                          line_margin=0.5, word_margin=0.1, boxes_flow=0.5,
                                                          detect_vertical=False, all_texts=False))
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
        miner_bbox = []
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
                        miner_bbox.append(bbox)
        all_miner_bbox.append(miner_bbox)
    return all_miner_bbox
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
def plumber(plum_file) -> 'list of pages as images':
    pdf = pdfplumber.open(plum_file)
    all_image = []
    for i, val in enumerate(pdf.pages):
        image = val.to_image(resolution=300)
        all_image.append(image)
    return all_image
        # image.draw_rects(plum_bbox)
        # image.save(f'a1.pdf')


in_file_loc = 'visualise_bbox_more_pages'
out_file_loc = 'visualise_bbox_more_pages'
for files in glob.glob(in_file_loc + '/*.pdf'):
    file_name = files.split("\\")[-1]
    file_name_only = file_name.split(".")[0]

    print(f'Parsing file: {file_name}')
    file = open(files, 'rb')
    all_bbox = miner(file)  # all bbox info
    images = plumber(file)
    assert len(images) == len(all_bbox), "all_bbox and images should be equal"
    if not os.path.exists(out_file_loc + '/' + file_name_only):
        os.mkdir(out_file_loc + '/' + file_name_only)
    out_file = out_file_loc + '/' + file_name_only + '/'
    for pos, img in enumerate(images):
        img.draw_rects(all_bbox[pos])
        img.save(f"{out_file}_{pos}.pdf")




from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.layout import LTTextBox, LTTextLine, LTChar, LTTextContainer
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

# output_string = StringIO()
# with open(file + '.pdf', 'rb') as in_file:
#     parser = PDFParser(in_file)
#     doc = PDFDocument(parser)
#     rsrcmgr = PDFResourceManager()
#     device = TextConverter(rsrcmgr, output_string, laparams=LAParams(line_overlap = 0.5, char_margin = 2.0,
#                         line_margin = 0.5, word_margin = 0.1, boxes_flow = 0.5,
#                         detect_vertical = False, all_texts = True))
#     interpreter = PDFPageInterpreter(rsrcmgr, device)
#     for page in PDFPage.create_pages(doc):
#         interpreter.process_page(page)
#
# # with open(file + ".txt", "wb") as f:
# #     f.write(output_string.getvalue().encode())
# #     f.close()
# print(output_string.getvalue())

def pdftotxt(path, output, new_name):
    # Create a pdf parser
    parser = PDFParser(path)
    # Create an object storing information
    document = PDFDocument(parser)
    # Evaluate if extractable
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # Create a PDF resource management to restore resource
        resmag = PDFResourceManager()
        # Set a parameter for analysis
        laparams = LAParams()
        # Create a PDF object
        # device = PDFDevice(resmag)
        device = PDFPageAggregator(resmag)
        # Create a PDF interpreter
        interpreter = PDFPageInterpreter(resmag, device)
        # Analyzing each page
        for page in PDFPage.get_pages(path):
            interpreter.process_page(page)
            # Assign LTPage of this page
            layout = device.get_result()
            p = device.receive_layout(page)
            for pos, element in enumerate(layout):
                if isinstance(element, LTTextContainer):
                    print(element.get_text())

            # for obj in layout._objs:
            #     if(isinstance(obj,LTChar)):
            #         # for o in obj._objs:
            #         #     if(isinstance(o, LTTextLine)):
            #         text = obj.get_text()
            #         print(text)
                        # else:
                        #     print('not')
                    # with open("%s"%(new_name),'a',encoding="utf-8") as f:
                    #     f.write(y.get_text()+"\n")
                    # print(y.get_text() + "\n")

# Get a PDF's directory to test
file_name = "foo.pdf"
file = file_name.split(".")[0]
filepath = open(file + '.pdf', 'rb')
output_string = StringIO()
pdftotxt(filepath, output_string, "pdfminer.txt")

# def createDeviceInterpreter():
#     rsrcmgr = PDFResourceManager()
#     laparams = LAParams()
#     device = PDFPageAggregator(rsrcmgr, laparams=laparams)
#     interpreter = PDFPageInterpreter(rsrcmgr, device)
#     return device, interpreter
#
# def parse_obj(objs):
#     for obj in objs:
#         if isinstance(obj, pdfminer.layout.LTTextBox):
#             for o in obj._objs:
#                 if isinstance(o,pdfminer.layout.LTTextLine):
#                     text=o.get_text()
#                     if text.strip():
#                         for c in  o._objs:
#                             if isinstance(c, pdfminer.layout.LTChar):
#                                 print "fontname %s"%c.fontname
#         # if it's a container, recurse
#         elif isinstance(obj, pdfminer.layout.LTFigure):
#             parse_obj(obj._objs)
#         else:
#             pass
#
# document=createPDFDoc("/tmp/simple.pdf")
# device,interpreter=createDeviceInterpreter()
# pages=PDFPage.create_pages(document)
# interpreter.process_page(pages.next())
# layout = device.get_result()


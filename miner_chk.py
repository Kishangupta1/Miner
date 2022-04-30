import pdfminer
import os
import glob
import time
in_path = "check"  # i/p dir
out_path = "others"  # o/p dir

for files in glob.glob(in_path + '/*.pdf'):
    print(f'\nparsing file: {files}')
    file = files.split("\\")[-1]
    file = file.split(".")[0]
    inp = in_path + "/" + file
    # out = out_path + "/" + file

    # file = "axa_replica.pdf"
    # file_name = file.split(".",1)[0]
    # if os.path.exists(file_name + ".txt"):
    #   os.remove(file_name + ".txt")

    from pdfminer.high_level import extract_pages
    from pdfminer.layout import LTTextContainer
    # from pdfminer.layout import LAParams

    start_time = time.time()
    print(f'start_time: {start_time}')

    for page_layout in extract_pages(files):
        for pos, element in enumerate(page_layout):
            if isinstance(element, LTTextContainer):
                # file = open(out + ".txt", "a", encoding="utf-8")
                # file.write("\ntext_blocks# " + str(pos+1) + "\n")
                # file.write(element.get_text())
                print(element.get_text())
                print(element.get_rect())
                # file.write(element.get_rect())
                # file.close()

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total_time:{total_time}")
    # break
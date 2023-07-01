from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage
from pdfminer.converter import PDFPageAggregator
import re
 
'''
    @brief Get all references msg from the given paper
'''
def get_references(paper_name, target_str="references"):
    fp = open(paper_name, 'rb')
    parser = PDFParser(fp)
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    document = PDFDocument(parser)
    
    text_content = []
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                text_content.append(lt_obj.get_text())
            else:
                pass
    
    
    # text_content 中每一个元素存储了一行文字
    total_text = ''.join(text_content).replace("\n","")
    start = len(total_text) - 1
    while start > 0:
        if total_text[start: start + 10].lower() == target_str.lower():
            print(total_text[start: start + 10])
            break
        else:
            start -= 1
    file = open("./output/tmp_output","w")
    write_data = total_text[start: len(total_text)]
    len_data = len(write_data)
    cur = 0
    while cur < len_data:
        tail = cur + 1
        while tail < len_data and write_data[tail] != '[':
            tail += 1
        write_line = write_data[cur: tail]
        file.write(write_line + "\n")
        cur = tail
    
    file.close()

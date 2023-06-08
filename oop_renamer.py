import os
import pytesseract
from pdf2image import convert_from_path
import re

#Поиск файлов в формате .pdf и возврат пути до файла этого формата
class PDFSearcher:
    def __init__(self, path):
         self.path = path

    def path_pdf_collect(self):
        pdf_pathes = []
        for PDFfile in os.listdir(self.path):
                if not PDFfile.lower().endswith('.pdf'):
                    continue
                else:
                    allPath = os.path.join(self.path, PDFfile)
                    pdf_pathes.append(allPath)
        return pdf_pathes

class ReSearcher:
    #Проверка регулярными выражениями
    def __init__(self, path, savetext):
         self.path = PDFSearcher(path=path)
         self.imgtotext = PdfImgToText()
         self.poppler_path = r'poppler-23.01.0\Library\bin'
         self.change_name_doc = NameChanges()
         self.savetext = savetext

    def re_namer(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pathes = self.path.path_pdf_collect()
        for path in pathes:
            converpath = convert_from_path(path, poppler_path=self.poppler_path)
            firstPage = converpath[0]
            firstPagetxt = pytesseract.image_to_string(firstPage, lang='rus')
            ReName = re.compile(r'Договор(.*)|Контракт(.*)|Соглашение(.*)', re.I) 
            name = ReName.search(firstPagetxt)
            name_doc = str(name.group(0))
            name_doc = self.change_name_doc.changer_signs(name_doc=name_doc)
            ReDate = re.compile(r'(\d{2}|\D\d{2}\D)[. ](.*)[. ](\d{4})')
            date = ReDate.search(firstPagetxt)
            date_doc = str(date.group(0))
            filename_end = self.change_name_doc.name_changer(path=path, 
                                              name_doc=name_doc, 
                                              date_doc=date_doc)
            if self.savetext == 'y':
                self.imgtotext.pdf_to_text(converpath, path, filename_end)
        return ('complete')
    
class NameChanges:

    def changer_signs(self, name_doc):
         if name_doc != None:
            invalidCharacters = re.compile(r'(\/)|(\:)|(\\)|(\*)|(\?)|(\")|(\<)|(\>)|(\|)')
            for symbol in name_doc:
                if invalidCharacters.search(symbol):
                    name_doc = name_doc.replace(symbol, '-')
            return name_doc  

    def name_changer(self, path, name_doc, date_doc):
        filename_end = f'{name_doc} {date_doc}'
        head_path, tail_path = os.path.split(path)
        fullPath = os.path.join(head_path, (filename_end + '.pdf'))
        os.rename(path, fullPath)
        return filename_end 

class PdfImgToText:
    def pdf_to_text(self, converpath, path, filename_end):
        DocTxt = ''

        for page_number, page_data in enumerate(converpath, start=1):
            txt = pytesseract.image_to_string(page_data, lang='rus')
            DocTxt += f"Page # {(str(page_number))} {txt}"
        
        head_path, tail_path = os.path.split(path)
        txtName = os.path.join(head_path, (filename_end +'.txt'))   
        with open(file=txtName, mode='w') as file:
            file.write(DocTxt)

if __name__ == '__main__':
    C = ReSearcher(r'C:\Users\glebg\Documents\tests', 'y')
    print(C.re_namer()) 


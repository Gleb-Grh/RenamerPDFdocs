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

#Конвертирование формата и чтение картинки pdf как текста 1 страница   
class ReaderText:
    def __init__(self, path):
        pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'
        self.converpath = convert_from_path(path, poppler_path=r'poppler-23.01.0\Library\bin')

    def convert_n_read_first_page(self):
        firstPagetxt = self.converpath[0]
        text = pytesseract.image_to_string(firstPagetxt, lang='rus')
        return text

#Поиск наименомания и даты договора    
class RegularExp:
    def __init__(self, text) -> None:
        self.text = text

    def name_exp(self):
        ReName = re.compile(r'Договор(.*)|Контракт(.*)|Соглашение(.*)', re.I) 
        name = ReName.search(self.text)
        name_doc = str(name.group(0))
        return name_doc
    
    def date_exp(self):
        ReDate = re.compile(r'(\d{2}|\D\d{2}\D)[. ](.*)[. ](\d{4})')
        date = ReDate.search(self.text)
        date_doc = str(date.group(0))
        return date_doc
    
#проверка и замена недопустимых символов при сохранении

class NameChanges:
    def changer_signs(self, name_doc):
         if name_doc != None:
            invalidCharacters = re.compile(r'(\/)|(\:)|(\\)|(\*)|(\?)|(\")|(\<)|(\>)|(\|)')
            for symbol in name_doc:
                if invalidCharacters.search(symbol):
                    name_doc = name_doc.replace(symbol, '-')
            return name_doc  

#формирование имени файла и переименование файлов в заданной папке
class FinalName:
    def name_changer(self, name_doc_change, date_doc):
        filename_end = f'{name_doc_change} {date_doc}'
        return filename_end
        
    def renamer(self, path, filename_end):
        head_path, tail_path = os.path.split(path)
        fullPath = os.path.join(head_path, (filename_end + '.pdf'))
        os.rename(path, fullPath)

# Сохранение текста из картинки pdf в txt файл
class PdfImgToText(ReaderText):
    def __init__(self, path):
        super().__init__(path)
        self.path = path

    def pdf_to_text(self, filename_end):
        DocTxt = ''
        for page_number, page_data in enumerate(self.converpath, start=1):
            txt = pytesseract.image_to_string(page_data, lang='rus')
            DocTxt += f"Page # {(str(page_number))} \n{txt}"
        
        head_path, tail_path = os.path.split(self.path)
        txtName = os.path.join(head_path, (filename_end +'.txt'))   
        with open(file=txtName, mode='w') as file:
            file.write(DocTxt)



if __name__ == '__main__':
     #Управляюший класс
    class Manage:
        def __init__(self, userpath, savetext):
            self.pathes = PDFSearcher(userpath).path_pdf_collect()
            self.name_doc_change = NameChanges()
            self.final_name = FinalName()
            self.savetext = savetext

        def manage(self):
            for path in self.pathes:
                text = ReaderText(path=path).convert_n_read_first_page()
                name_doc = RegularExp(text=text).name_exp()
                name_doc_change = self.name_doc_change.changer_signs(name_doc=name_doc)
                date_doc = RegularExp(text=text).date_exp()
                filename_end = self.final_name.name_changer(name_doc_change=name_doc_change, date_doc=date_doc)
                if self.savetext == 'y':
                    PdfImgToText(path=path).pdf_to_text(filename_end=filename_end)
                self.final_name.renamer(path=path, filename_end=filename_end)
            
    Manage(r'C:\Users\glebg\Documents\tests','n').manage()

          
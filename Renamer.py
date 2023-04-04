#Python3
import os
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import re
 

def renamer(filePath, converpath, savetxt):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    path, filename = os.path.split(filePath)
    fileBaseName, fileExtension = os.path.splitext(filename)
    firstPage = converpath[0]
    firstPagetxt = pytesseract.image_to_string(firstPage, lang='rus')
    ReCon = re.compile(r'Договор(.*)|Контракт(.*)|Соглашение(.*)', re.I) 
    match = ReCon.search(firstPagetxt)
    ReDate = re.compile(r'(\d{2}|\D\d{2}\D) (.*) (\d{4})')
    date = ReDate.search(firstPagetxt)

    #Searching and renaming invalid characters
    nameDoc = str(match.group(0))
    invalidCharacters = re.compile(r'(\/)|(\:)|(\\)|(\*)|(\?)|(\")|(\<)|(\>)|(\|)')
    for symbol in nameDoc:
        if invalidCharacters.search(symbol):
            nameDoc = nameDoc.replace(symbol, '-')  
    filename_end = f'{nameDoc} {str(date.group(0))}'
    fullPath = path + '\\' + filename_end + fileExtension
    os.rename(filePath, fullPath)

    def PDFimgtoTXT():
        DocTxt = ''
        for page_number, page_data in enumerate(converpath, start=1):
            txt = pytesseract.image_to_string(page_data, lang='rus')
            DocTxt += f"Page # {(str(page_number))} {txt}"

        txtName = path + '\\' + filename_end + '.txt'   
        with open(file=txtName, mode='w') as file:
            file.write(DocTxt)
    if savetxt == 'y':
        PDFimgtoTXT()


def main():
    print("""Укажите полный путь файла в формате pdf, 
содержащего отсканированный текст договора/соглашения/контракта 
для автоматического переименования файла:""")
    filePath = input()
    converpath = convert_from_path(filePath, poppler_path=r'C:\code\ContraktName_fromPDF\env\Lib\site-packages\poppler-23.01.0\Library\bin')
    print('''Потребуется ли сохранить текст из изображения y/n?''')
    savetxt = input()
    renamer(filePath=filePath, converpath=converpath, savetxt=savetxt)

if __name__ == '__main__':
    main()


import tkinter as tk
from tkinter import messagebox  
from oop_renamer_v2 import *

win = tk.Tk()
photo = tk.PhotoImage(file='icon.png') 
win.iconphoto(False, photo)
win.config(background='light blue')
win.title('Renamer for legal')
win.geometry(f"560x400+100+200")
win.resizable(True, True)

label1 = tk.Label(win, text='''Укажите путь до папки с файлами, 
содержащими отсканированный текст договора/соглашения/контракта 
для автоматического переименования файлов:''', 
                    bg='light blue',
                    font=('Arial', 10),
                    padx=10,
                    pady=10,  
                    width=70,
                    height=4,  
                    justify=tk.CENTER,
                    )
label1.grid(row=0, column=0)

path_user = tk.Entry(win,
                width=50)
path_user.grid(row=1, column=0)



savetext_vidj_val = tk.StringVar()
savetext_vidj = tk.Checkbutton(win, 
                               text='Потребуется ли сохранить текст из изображения?',
                               bg='light blue',
                               variable=savetext_vidj_val,
                               offvalue='n',
                               onvalue='y',
                               )
savetext_vidj.grid(row=2, column=0, sticky='we')

label3 = tk.Label(win, 
                  text='',
                  bg='light blue',
                  width=70, 
                  height=3,
                  justify=tk.LEFT,)
label3.grid(row=3, column=0)


label4 = tk.Label(win, 
                  
text='''
    Для работы приложения необходимо установить приложение распознования текста 
    tesseract на свой компьютер в директорию:
    C:/Program Files/Tesseract-OCR/tesseract.exe 
    скачать версию 3.2.1 можно по адресу:
    https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.1.20230401.exe''',
                  bg='light blue',
                    font=('Arial', 10),
                    padx=10, 
                    pady=13,  
                    width=70, 
                    height=7,  
                    justify=tk.LEFT,
                    
                  )
label4.grid(row=6, column=0, sticky='s')

pathes_gen = []
def start():
  filePath = path_user.get()
  P = PDFSearcher(path=filePath)
  pathes = P.path_pdf_collect()
  messagebox.showinfo('Список файлов pdf', pathes)
  global pathes_gen
  pathes_gen = (p for p in pathes)
  


btn1 = tk.Button(win, text = 'Поиск pdf',
                 command=start,
                 bg='red',
                )
btn1.grid(row=4,
          column=0,
          padx=5, 
          pady=5,)      

def iter():
  try:
    path = next(pathes_gen)
    text = ReaderText(path=path).convert_n_read_first_page()
    name_doc = RegularExp(text=text).name_exp()
    name_doc_change = NameChanges().changer_signs(name_doc=name_doc)
    date_doc = RegularExp(text=text).date_exp()
    filename_end = FinalName().name_changer(name_doc_change=name_doc_change, date_doc=date_doc)
    label3['text'] = path
    if savetext_vidj_val.get() == 'y':
      PdfImgToText(path=path).pdf_to_text(filename_end=filename_end)
    FinalName().renamer(path=path, filename_end=filename_end)
    win.after(1000, iter)
  except StopIteration:
    pass
btn2 = tk.Button(win, text = 'ПУСК',
                 command=iter,
                 bg='blue',
                )
btn2.grid(row=5,column=0,
          padx=5, 
          pady=5,) 

if __name__ == '__main__':
  win.mainloop()
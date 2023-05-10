import tkinter as tk  
from Renamer import renamer


def get_path():
    filePath = path.get()
    savetext = savetext_vidj_val.get()
    if filePath:
        global btntext
        renamer(filePath=filePath, savetxt=savetext)
        btn1['text'] = 'Завершено'
    else:
        message = tk.Label(win, text='Укажите путь', bg='blue', fg='white')
        message.grid(row=4, column=0,)


win = tk.Tk()
photo = tk.PhotoImage(file='icon.png') 
win.iconphoto(False, photo)
win.config(background='light gray')
win.title('Renamer for legal')
win.geometry(f"560x330+100+200")
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

path = tk.Entry(win,
                width=50)
path.grid(row=1, column=0)

savetext_vidj_val = tk.StringVar()
savetext_vidj = tk.Checkbutton(win, 
                               text='Потребуется ли сохранить текст из изображения?',
                               bg='light blue',
                               variable=savetext_vidj_val,
                               offvalue='n',
                               onvalue='y',
                               )
savetext_vidj.grid(row=3, column=0, sticky='we')

label3 = tk.Label(win, 
                  text='',
                  bg='light gray',
                  padx=10,
                  pady=10)
label3.grid(row=4, column=0)

btntext = 'Пуск'
btn1 = tk.Button(win, text = btntext,
                 command=get_path,
                 bg='red',
                )
btn1.grid(row=5,column=0)

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

win.mainloop()
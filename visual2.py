from tkinter import *
from tkinter.ttk import *

def _Btn(param, text):
    text.delete('1.0', END)
    print(param)
    text.insert(END, param)

def main():
    win = Tk()
    #win.geometry('500x500') # ширина=500, высота=400, x=300, y=200
    textFrame = Frame(win)
    entryLabel = Label(textFrame)
    entryLabel["text"] = "Enter the website:"
    entryLabel.grid(row=0, column=0, padx=2, pady=2)
    entryWidget = Entry(textFrame)
    entryWidget["width"] = 21
    entryWidget.grid(row=0, column=1, padx=2, pady=2)
    textFrame.grid(row=0, column=0, columnspan=2, sticky=N+S+E+W)

    scroll = Scrollbar(win)
    text = Text(win, height=20, width=40)
    scroll.grid(row=3, column=3, sticky=N+S+E+W)
    text.grid(row=3, column=0, columnspan=2)
    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)

    download = Button(win, text="Загрузить")
    download.grid(row=1, column=0, padx=2, pady=2, sticky=N+S+E+W)
    download["command"] = lambda: _Btn(entryWidget.get(), text)
    showfromdb = Button(win, text="Показать из базы")
    showfromdb.grid(row=1, column=1, padx=2, pady=2, sticky=N+S+E+W)
    showfromdb["command"] = lambda: _Btn(entryWidget.get(), text)

    list1 = [u"Один",u"Два",u"Три"]
    combobox = Combobox(win, values = list1, state='readonly', style='TButton', justify='center')
    combobox.set(u"Один") # Пункт по умолчанию
    combobox.grid(row=2, column=1, padx=2, pady=2, sticky=N+S+E+W)
    choice = Button(win, text="Выбрать") # создаём кнопку
    choice["command"] = lambda: _Btn(combobox.get(), text)
    choice.grid(row=2, column=0, padx=2, pady=2, sticky=N+S+E+W)

    #scroll = Scrollbar(win)
    #text = Text(win, height=20, width=40)
    #scroll.grid(row=3, column=3, sticky=N+S+E+W)
    #text.grid(row=3, column=0, columnspan=2)
    #scroll.config(command=text.yview)
    #text.config(yscrollcommand=scroll.set)
    quote = """HAMLET: To be, or not to be--that is the question:
    Whether 'tis nobler in the mind to suffer
    The slings and arrows of outrageous fortune
    Or to take arms against a sea of troubles
    And by opposing end them. To die, to sleep--
    No more--and by a sleep to say we end
    The heartache, and the thousand natural shocks
    That flesh is heir to. 'Tis a consummation
    Devoutly to be wished."""
    #text.insert(END, quote)
    win.mainloop()
if __name__ == '__main__':
    main()



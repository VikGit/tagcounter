from tkinter import *
from tkinter.ttk import *

def _Btn(param):
    print(param)
def main():
    win = Tk()
    win.geometry('500x500') # ширина=500, высота=400, x=300, y=200
    frame = Frame(win)
    frame.grid(row=0, column=0)
    frameBtn = Frame(win)
    frameBtn.grid(row=0, column=1)
    list1 = [u"Один",u"Два",u"Три"]
    combobox = Combobox(frame, values = list1, state='readonly', style='Kim.TButton')
    combobox.set(u"Один") # Пункт по умолчанию
    combobox.grid(row=0, column=0)
    button = Button(frameBtn, text=u"-- Моя кнопка --") # создаём кнопку
    button["command"] = lambda: _Btn(combobox.get())
    button.pack()
    win.mainloop()
if __name__ == '__main__':
    main()



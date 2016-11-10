from tkinter import *
from tkinter.ttk import *

def _Btn(param):
    print(param)
def displayText():
    """ Display the Entry text value. """

    global entryWidget

    if entryWidget.get().strip() == "":
        tkMessageBox.showerror("Tkinter Entry Widget", "Enter a text value")
    else:
        tkMessageBox.showinfo("Tkinter Entry Widget", "Text value =" + entryWidget.get().strip())
def main():
    win = Tk()
    win.geometry('500x500') # ширина=500, высота=400, x=300, y=200
    frame = Frame(win)
    frame.grid(row=0, column=0)
    frameBtn = Frame(win)
    frameBtn.grid(row=0, column=1)
    textFrame = Frame(win)
    list1 = [u"Один",u"Два",u"Три"]
    combobox = Combobox(frame, values = list1, state='readonly', style='Kim.TButton')
    combobox.set(u"Один") # Пункт по умолчанию
    combobox.grid(row=0, column=0)
    button = Button(frameBtn, text="Выбрать") # создаём кнопку
    button["command"] = lambda: _Btn(combobox.get())
    button.pack()
    button = Button(frameBtn, text="Выбрать") # создаём кнопку
    button["command"] = lambda: _Btn(combobox.get())
    button.pack()
    entryLabel = Label(textFrame)
    entryLabel["text"] = "Enter the text:"
    entryLabel.pack(side=TOP)
    entryWidget = Entry(textFrame)
    entryWidget["width"] = 50
    entryWidget.pack(side=LEFT)
    textFrame.pack()
    button = Button(win, text="Submit", command=displayText)
    button.pack()
    win.mainloop()
if __name__ == '__main__':
    main()



from tkinter import *
import serial
from tkinter import scrolledtext

ports = serial.tools.list_ports.comports()
def print_info():
    global txt2
    txt2.delete(1.0, END)
    txt2.insert(INSERT, "За один раз=")
    txt2.insert(INSERT, str(Sost.counter))
    txt2.insert(INSERT, "\nЗа все время=")
    txt2.insert(INSERT, str(Sost.allcounter))
class Sost:
    counter = 0
    allcounter = 0

    def __init__(self, parent, width, height, title="Состояние", resizable=(False, False), icon=None):
        self.root = Toplevel(parent)
        self.root.title(title)

        self.root.geometry(f"{width}x{height}+0+300")
        self.root.resizable(resizable[0], resizable[1])
        if icon:
            self.root.iconbimap(icon)

        self.root.title("Окно состояния")
        global ports
        readlab = Label(self.root, text="Номера com портов")
        readlab.grid(column=200, row=0)
        self.root.geometry('500x450')
        txt = scrolledtext.ScrolledText(self.root, width=20, height=10)
        txt.grid(column=200, row=2000)
        txt1 = scrolledtext.ScrolledText(self.root, width=20, height=10)
        txt1.grid(column=400, row=2000)
        txt.insert(INSERT,"Для ввода:\n")
        txt.insert(INSERT,ports[0].device)
        txt.insert(INSERT, "\n")
        txt.insert(INSERT, ports[3].device)

        txt1.insert(INSERT, "Для вывода:\n")
        txt1.insert(INSERT, ports[1].device)
        txt1.insert(INSERT, "\n")
        txt1.insert(INSERT, ports[2].device)

        readlab1 = Label(self.root, text="Количество переданных байт ")
        readlab1.grid(column=200, row=6000)
        global txt2
        txt2 = scrolledtext.ScrolledText(self.root, width=20, height=10)
        txt2.grid(column=200, row=9900)
        print_info()
        inputbutton = Button(self.root, text="Обновить", command=print_info)
        inputbutton.grid(column=400, row=30)






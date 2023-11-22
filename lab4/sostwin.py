from tkinter import *
import serial
from tkinter import scrolledtext
ports = serial.tools.list_ports.comports()

def print_max_kol():
    global txt2
    txt2.delete(1.0, END)
    txt2.insert(INSERT, "Максимальное количество попыток")
def print_collision(is_collision):
    global txt2
    if is_collision==1:
        txt2.delete(1.0, END)
        txt2.insert(INSERT, "Коллизия")
    else:
        txt2.delete(1.0, END)
        txt2.insert(INSERT, "Коллизии не обнаруженно")

def print_time(transmission_time):
    global txt1
    txt1.delete(1.0, END)
    txt1.insert(INSERT, f"Waiting for {transmission_time}s...")
def print_info():
    global txt2
    global txt3
    txt3.delete(1.0, END)
    txt3.insert(INSERT, "")
    txt3.insert(INSERT, str(Sost.readpacket))
    #lr4
    if Sost.is_busy==1:
        txt2.delete(1.0, END)
        txt2.insert(INSERT, "Канал занят, повторите отправку позже")
    if Sost.is_busy == 0:
        txt2.delete(1.0, END)
        txt2.insert(INSERT, "Канал свободен")
class Sost:
    counter = 0
    allcounter = 0
    readpacket=0
    is_busy=0
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
        txt = scrolledtext.ScrolledText(self.root, width=15, height=10)
        txt.grid(column=200, row=2000)
        global txt1
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

        qw = Label(self.root, text="Пакет до дебит стаффинга ")
        qw.grid(column=100, row=1000)
        global txt3
        txt3 = scrolledtext.ScrolledText(self.root, width=26, height=10)
        txt3.grid(column=100, row=2000)

        print_info()
        inputbutton = Button(self.root, text="Обновить", command=print_info)
        inputbutton.grid(column=400, row=30)







from array import array
import serial.tools.list_ports
import serial

import childwindow
from childwindow import ChildWindow
from controlwin import Controll
from time import sleep
from threading import Thread
from tkinter import ttk
from tkinter import *
from sostwin import Sost

for porta in childwindow.ports:
    print(porta.device)
port = childwindow.ports[0].device
baudrate = 9600
ser = serial.Serial(port, baudrate=baudrate)


def chooseports(event):
    global port, ser, baudrate, comboboxs, data
    selection = comboboxs.get()
    choseprts = selection.split('-')
    print(choseprts)
    if choseprts[1] == childwindow.ports[3].device:
        port = choseprts[1]
        print(port)
    else:
        if choseprts[0] == childwindow.ports[0].device:
            port = choseprts[0]
            print(port)
    ser.close()
    ser = serial.Serial(port, baudrate=baudrate, parity=serial.PARITY_EVEN)

def inputfunc(enum):  # Data to be sent, should be in bytes
    global text
    message = text.get()
    b = bytes(message, 'utf-8')
    Sost.counter=ser.write(b)
    Sost.allcounter+=Sost.counter
    text.delete(0, END)


class Window:
    def __init__(self, width, height, title="Запись", resizable=(False, False), icon=None):
        self.root = Tk()
        self.root.title(title)

        self.root.geometry(f"{width}x{height}+0+0")
        self.root.resizable(resizable[0], resizable[1])
        if icon:
            self.root.iconbimap(icon)
        inputlabl = Label(self.root, text="Введите данные для передачи через com порт")
        inputlabl.grid(column=0, row=0)
        global text
        text = Entry(self.root, width=30)
        text.grid(column=0, row=20)
        text.bind("<Return>", inputfunc)
        messege = text.get()
        #inputbutton = Button(self.root, text="Отправить", command=inputfunc)
        #inputbutton.grid(column=0, row=30)

        global comboboxs
        comboboxs = ttk.Combobox(self.root, values=childwindow.combined_ports)
        comboboxs.grid(column=0, row=40)
        comboboxs.bind("<<ComboboxSelected>>", chooseports)

    def run(self):
        self.root.mainloop()

    def create_child(self, width, height, title="Чтение", resizable=(False, False), icon=None):
        ChildWindow(self.root, width, height, title, resizable, icon)

    def create_control(self, width, height, title="Контроль", resizable=(False, False), icon=None):
        Controll(self.root, width, height, title, resizable, icon)

    def create_Sost(self, width, height, title="Состояние", resizable=(False, False), icon=None):
        Sost(self.root, width, height, title, resizable, icon)


if __name__ == "__main__":
    window = Window(400, 200)
    window.create_control(500, 500)
    window.create_child(200, 100)
    window.create_Sost(400, 400)
    window.run()

ser.close()

from base64 import decode
from tkinter import *
from tkinter import ttk
import threading
import serial.tools.list_ports
from tkinter import scrolledtext
import serial
from base64 import decode
import packSend
from packSend import MyFrame

import controlwin
global ports,porrs
ports = serial.tools.list_ports.comports()
porrs = ports[1].device
baudrate = 9600
global par
par=serial.PARITY_EVEN
print(controlwin.par_value)
serw = serial.Serial(porrs, baudrate=baudrate,parity=par)

def chooseport(event):
    global porrs,serw,baudrate,ports,combobox,data
    selection = combobox.get()
    choseprt = selection.split('-')
    if choseprt[1]==ports[1].device:
        porrs=choseprt[1]
        print(porrs)
    else:
         if choseprt[0]==ports[2].device:
             porrs = choseprt[0]
             print(porrs)
    data=b"p"
    serw.close()
    global par
    print(controlwin.par_value)
    if (controlwin.par_value == "нечетный"):
        par = serial.PARITY_EVEN
    else:
        if(controlwin.par_value == "четный"):
            par = serial.PARITY_ODD
        else:
            if(controlwin.par_value=="Нет паритета"):
                par=serial.PARITY_NONE
            else:
                if (controlwin.par_value=="Установлен в mark"):
                    par=serial.PARITY_MARK
                else:
                    if(controlwin.par_value=="Установлен в space"):
                        par=serial.PARITY_SPACE

    serw = serial.Serial(porrs, baudrate=baudrate, parity=par)
    print(par)

global combined_ports
combined_ports = ""

for i in range(0, len(ports), 2):
    # Если достаточно портов для создания пары
    if i + 1 < len(ports):
        combined_ports += ports[i].device + "-" + ports[i + 1].device + " "

# Убираем последний пробел
combined_ports = combined_ports.rstrip()

global data
def deletetext():
    global txt
    txt.delete(1.0, END)

reading_active = True

def convert_list_to_message(message_list):
    message = ''

    # Итерируемся по числам в списке
    for char_code in message_list:
        # Преобразуем числовой код в соответствующий символ
        char = chr(char_code)
        message += char

    return message

def debyte_stuffing(packet):
    unstuffed_data = []
    esc = 27
    z = ord('z') + 3
    i = 0
    while i < len(packet.data):
        if packet.data[i] == esc:
            i += 1
            unstuffed_data.append(z)
        else:
            unstuffed_data.append(packet.data[i])
            i += 1

    packet.data = bytes(unstuffed_data)


def reads():
    global txt,data,reading_active
    data=""
    stop=b"p"
    parity_type = "нечетный"
    while reading_active:

        received_frame = packSend.receive_frame(serw)
        print("Source Address")
        print(received_frame.source_address)
        debyte_stuffing(received_frame)
        #print(mes)
        received_frame = convert_list_to_message(received_frame.data)
        txt.insert(INSERT, received_frame)
        if data == stop:
            break
def readfunc():
    global reading_active
    reading_active = True
    thread = threading.Thread(target=reads)
    thread.start()

def stop_reading():
    global reading_active
    reading_active = False
class ChildWindow:
    def __init__(self,parent,width,height,title="Чтение",resizable=(False,False),icon=None):
        self.root = Toplevel(parent)
        self.root.title(title)
        self.root.geometry(f"{width}x{height}+500+0")
        self.root.resizable(resizable[0],resizable[1])
        readlabl = Label(self.root, text="Данные полученные через com порт")
        readlabl.grid(column=0, row=0)
        self.root.geometry('500x450')
        global txt
        txt = scrolledtext.ScrolledText(self.root, width=40, height=10)
        txt.grid(column=0, row=20)
        readbutton = Button(self.root, text="прочитать", command=readfunc)
        delbutton = Button(self.root,text = "очистить",command=deletetext)
        stopread = Button(self.root, text="Прекратить чтение", command=stop_reading)
        stopread.grid(column=3, row=30)
        delbutton.grid(column=3, row=20)
        readbutton.grid(column=3, row=10)
        global combobox
        combobox = ttk.Combobox(self.root,values=combined_ports)
        combobox.grid(column=0, row=220)
        combobox.bind("<<ComboboxSelected>>", chooseport)

        if icon:
            self.root.iconbimap(icon)
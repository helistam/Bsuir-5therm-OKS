import random
from array import array
import serial.tools.list_ports
import serial

import packSend
from packSend import MyFrame

import re
import childwindow
from childwindow import ChildWindow
from controlwin import Controll
from time import sleep
from threading import Thread
from tkinter import ttk
from tkinter import *
from sostwin import Sost, print_max_kol, print_info

polynomial = [int(bit) for bit in "100101"]#x5+x2+1
def string_to_bits(string):
    # Преобразование каждого символа в ASCII-код и получение его бинарного представления
    bits = [format(ord(char), '08b') for char in string]
    # Объединение всех бинарных представлений в одну строку
    bit_string = ''.join(bits)
    # Преобразование строки из битов в список целых чисел
    return [int(bit) for bit in bit_string]

def CRCcode(StrToCode):
    message_bits = string_to_bits(StrToCode)
    crc_hash=calculate_hash(message_bits)
    print("CRC_CASH",crc_hash)
    print("Message+CRC_CASH")
    print(message_bits+crc_hash)

    return crc_hash
def calculate_hash(message: list[int]) -> list[int]:#тип возвращаемого значения
    hash_len = len(polynomial) - 1# т.к. строка делаем -1
    align_len = len(message) - 1

    reminder = message.copy() + [0] * hash_len #делимое с доп нулями
    divisor = polynomial.copy() + [0] * align_len# делитель

    for i, _ in enumerate(message):#это функция, которая создает итератор, возвращающий пары (индекс, элемент) для элементов в message
        if reminder[i] == divisor[i] == 1:
            reminder = [x ^ y for x, y in zip(reminder, divisor)]#zip- генератор кортежа: пример [1,0] и [0,1]==[(1,0),(0,1)]                                                                #^- побитовый xor для элементов списка
        divisor.pop() # cдивиг элементов делителя на 1 влево( чтобы делилось в столбик)
        divisor.insert(0, 0)

    return reminder[-hash_len:]


for porta in childwindow.ports:
    print(porta.device)
port = childwindow.ports[0].device
baudrate = 9600
ser = serial.Serial(port, baudrate=baudrate,parity=serial.PARITY_EVEN)
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

def convertToSend(mes):
    message_list = []
    # Проверяем, что message не пустое
    if mes:
        # Итерируемся по символам в сообщении
        for char in mes:
            # Преобразуем символ в его числовое представление (ASCII-код)
            char_code = ord(char)
            message_list.append(char_code)

    return message_list

def get_com_port_number(port_name):
    match = re.search(r'\d+', port_name)
    if match:
        return int(match.group())
    return None

def byte_stuffing(packet):
    stuffed_data = []
    esc = 27  # Представляем символ "Escape" как байт
    for byte in packet.data:
        if byte == packet.flag:
            stuffed_data.append(esc)  # Заменяем на esc
        else:
            stuffed_data.append(byte)

    packet.data = stuffed_data
def inputfunc(enum):  # Data to be sent, should be in bytes
    global text
    message = text.get()
    portNum = get_com_port_number(port)
    # Разбиваем строку на порции по 3 символа
    message_chunks = [message[i:i+3] for i in range(0, len(message), 3)]
    for chunk in message_chunks:
        FCS = CRCcode(chunk)

        ascii_code = int(''.join(map(str, FCS)), 2)
        # Преобразование ASCII-кода в символ
        char_FCS = ascii_code

        print("NEW CHAR",char_FCS)
        message_list = convertToSend(chunk)

        # Дополняем message_list нулями, если нужно
        while len(message_list) < 3:
            message_list.append(0)
        frame_to_send = MyFrame(source_address=portNum, data=message_list, fcs=char_FCS)
        byte_stuffing(frame_to_send)
        stuffed_data = frame_to_send.packs()

        #lr4
        packSend.clear_try_counter()
        is_busy=random.choice([True, False])
        if is_busy==False:
            Sost.is_busy = 0
            print_info()
            packSend.send_frame(ser, stuffed_data)
            text.delete(0, END)
            packSend.wait_transmission_time()#предположительное время пока кадр дойдет до канала
            if packSend.simulate_collision():
                packSend.send_jam(ser)
                packSend.wait_transmission_time()

                packSend.increment_try_counter()
                if packSend.is_try_counter_max():
                    print_max_kol()
                packSend.calculate_and_wait_random_delay()
                packSend.send_frame(ser, stuffed_data)


            Sost.allcounter += Sost.counter
            text.delete(0, END)
        else :
            Sost.is_busy=1
            print_info()



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
    window.create_Sost(500, 400)
    window.run()

ser.close()

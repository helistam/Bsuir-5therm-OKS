import re
import threading
from concurrent.futures import thread
from time import sleep
from tkinter import END

import serial.tools.list_ports
import serial

import Marker
import packSend

allports = serial.tools.list_ports.comports()
first_port = allports[4].device#8
second_port=allports[1].device#9
third_port=allports[2].device#12

baudrate = 9600

global is_marker_here,where_is_marker,markerInfo
markerInfo=1
where_is_marker=0
is_marker_here=0

first_connect = serial.Serial(first_port, baudrate=baudrate,bytesize=8, parity='N',
                              stopbits=1, timeout=1, xonxoff=False, rtscts=False)
second_connect=serial.Serial(second_port, baudrate=baudrate,bytesize=8, parity='N',
                              stopbits=1, timeout=1, xonxoff=False, rtscts=False)
third_connect=serial.Serial(third_port, baudrate=baudrate,bytesize=8, parity='N',
                              stopbits=1, timeout=1, xonxoff=False, rtscts=False)

# def get_com_port_number(port_name):
#     match = re.search(r'\d+', port_name)
#     if match:
#         return int(match.group())
#     return None
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

def GenerateMark():
    wait_correct_port = threading.Thread(target=waitPort, daemon=True)
    wait_correct_port.start()
    global is_marker_here
    markToSend = Marker.Markers(SD=1,AC=0,ED=1)
    markToSend = markToSend.packs()
    is_marker_here=0
    Marker.send_Marker(first_connect, markToSend)
    is_marker_here=0


marker_event = threading.Event()

global enum1,text1,sendAdrr1,SourceAddress1,priority1,priority2,priority3,priority
priority=0
priority1=0
priority2=0
priority3=0
sendAdrr1=0
enum1=0
text1=0
SourceAddress1=0
def waitPort():
    global where_is_marker
    while text1==0:
        sleep(4.5)
    while 1:
        while where_is_marker != sendAdrr1:
            marker_event.wait()  # Ждем, пока событие не будет установлено
            marker_event.clear()
        if where_is_marker == sendAdrr1:
            Send_func(enum1,text1,sendAdrr1,SourceAddress1)
            where_is_marker=0
def Send_func(enum,text,sendAdrr,SourceAddress):
    global is_marker_here,where_is_marker,markerInfo,enum1,text1,sendAdrr1,SourceAddress1
    enum1=enum
    text1=text
    sendAdrr1=sendAdrr
    SourceAddress1=SourceAddress


    sendAdrrs=sendAdrr
    print(SourceAddress)
    print("Адрес окна",sendAdrr)
    message = text.get()
    #print(message)


    if where_is_marker==sendAdrr and message!="":
        is_marker_here = 1

        print(f"SENDER PRIORITET={priority}")
        if priority==1:
            markerInfo.AC=0b00110000
        else:
            markerInfo.AC = 0b01010000


        message_chunks = [message[i:i + 3] for i in range(0, len(message), 3)]#разбиваем строку на чанки по 3 символа
        for chunk in message_chunks:
            message_list = convertToSend(chunk)
            # Дополняем message_list нулями, если нужно
            while len(message_list) < 3:
                message_list.append(0)
            frame_to_send = packSend.MyFrame(source_address=SourceAddress, data=message_list,dest_adress=sendAdrr,SD=markerInfo.SD,AC=markerInfo.AC,ED=markerInfo.ED,FS=0b00000000)
            stuffed_data = frame_to_send.packs()
            print("Otladka")
            print(frame_to_send.data)
            print(stuffed_data)
            if SourceAddress==1:
                packSend.send_frame(first_connect, stuffed_data)
            else:
                if SourceAddress == 2:
                    packSend.send_frame(second_connect,stuffed_data)
                else:
                    if SourceAddress == 3:
                        packSend.send_frame(third_connect,stuffed_data)
        #is_marker_here=0
        text.delete(0, END)
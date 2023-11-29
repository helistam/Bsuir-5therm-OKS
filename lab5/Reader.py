import threading
from time import sleep
from tkinter import INSERT

import Marker
import packSend
import serial.tools.list_ports
import serial
import Sender

allports = serial.tools.list_ports.comports()
first_port = allports[0].device#7
second_port=allports[3].device#10
third_port=allports[5].device#11
baudrate = 9600
first_connect = serial.Serial(first_port, baudrate=baudrate,)
second_connect=serial.Serial(second_port, baudrate=baudrate)
third_connect=serial.Serial(third_port, baudrate=baudrate)

global txt1,txt2,txt3
global choose_ports,counter,debug_texts,delete_marker
delete_marker=0
counter=0
def bytes_to_bits(byte_data):
    return ''.join(format(byte, '08b') for byte in byte_data)
def convert_list_to_message(message_list):
    message = ''

    # Итерируемся по числам в списке
    for char_code in message_list:
        # Преобразуем числовой код в соответствующий символ
        char = chr(char_code)
        message += char

    return message

def reads():
    global txt1,txt2,txt3
    global choose_ports,delete_marker

    if choose_ports==1:#станция которая читает
        while 1:
            mark_received=Marker.receive_Marker(first_connect)
            Sender.markerInfo=mark_received

            AC = mark_received.AC.to_bytes(1, byteorder='little')
            AC = bytes_to_bits(AC)

            LevelOfPriority = AC[:3]
            LevelOfPriority = int(LevelOfPriority, 2)# уровень приоритета

            print(Sender.markerInfo.AC)
            prioritet=bytes_to_bits(Sender.markerInfo.AC.to_bytes(1, byteorder='little'))

            if Sender.priority==Sender.priority1:

                if AC[3] == '1':

                    Sender.where_is_marker = 1
                    received_frame = packSend.receive_frame(first_connect)

                    fs_bytes = received_frame.FS.to_bytes(1, byteorder='little')
                    fs_bits = bytes_to_bits(fs_bytes)


                    dest_addr = received_frame.destination_address
                    debug_texts.insert(INSERT, f"Станция1: Получен кадр с Destination Address={dest_addr}\n")
                    #print(f"Source Adress:{received_frame.source_address}")

                    if(received_frame.source_address==1 and  fs_bits=='10010000'):
                        debug_texts.insert(INSERT, "Станция1: Кадр прошедший круг был прочитан\n")

                        if delete_marker==0:
                            debug_texts.insert(INSERT, "Станция1: Запускаю новый(пустой) токен\n")
                            markToSend = Marker.Markers(SD=1, AC=0, ED=1)
                            markToSend = markToSend.packs()
                            Sender.is_marker_here = 0
                            Marker.send_Marker(Sender.first_connect, markToSend)
                        else:
                            debug_texts.insert(INSERT, "Станция1: Маркер удален\n")
                    else:

                        if dest_addr==1:
                            fullpacket = received_frame
                            received_frame = convert_list_to_message(received_frame.data)

                            fullpacket.FS = 0b10010000  # утсановка что прочитано
                            frame_to_send = packSend.MyFrame(source_address=fullpacket.source_address, data=fullpacket.data,
                                                             dest_adress=fullpacket.destination_address, SD=0, AC=0b00010000, ED=0,
                                                             FS=fullpacket.FS)
                            stuffed_data = frame_to_send.packs()
                            packSend.send_frame(Sender.first_connect, stuffed_data)
                            txt1.insert(INSERT, received_frame)
                        else:
                            frame_to_send = packSend.MyFrame(source_address=received_frame.source_address, data=received_frame.data, dest_adress=received_frame.destination_address,SD=0,AC=0b00010000,ED=0,FS=received_frame.FS)
                            stuffed_data = frame_to_send.packs()
                            sleep(1)
                            packSend.send_frame(Sender.first_connect, stuffed_data)
                else:
                    Sender.where_is_marker = 1
                    Sender.marker_event.set()
                    sleep(1)
                    if(Sender.is_marker_here==0):
                        mark_received.AC = Sender.markerInfo.AC
                        mark_received = mark_received.packs()
                        if delete_marker == 0:
                            Marker.send_Marker(Sender.first_connect,mark_received)
                            debug_texts.insert(INSERT, "Станция1: Получен пустой токен\n")
                        else:
                            debug_texts.insert(INSERT, "Станция1: Удален пустой токен\n")

            else:
                mark_received.AC = Sender.markerInfo.AC
                mark_received = mark_received.packs()
                if delete_marker == 0:
                    Marker.send_Marker(Sender.first_connect, mark_received)
                debug_texts.insert(INSERT, "Станция1: Приоритет станции ниже приоритета маркера \n")
    if choose_ports == 2:
        while 1:
            mark_received2 = Marker.receive_Marker(second_connect)
            Sender.markerInfo = mark_received2

            AC= mark_received2.AC.to_bytes(1, byteorder='little')
            AC = bytes_to_bits(AC)

            if Sender.priority==Sender.priority2:

                if AC[3] == '1':

                    Sender.where_is_marker = 2
                    received_frame = packSend.receive_frame(second_connect)

                    fs_bytes = received_frame.FS.to_bytes(1, byteorder='little')
                    fs_bits = bytes_to_bits(fs_bytes)

                    #print(f"FS={ fs_bits}")


                    dest_addr = received_frame.destination_address
                    debug_texts.insert(INSERT, f"Станция2: Получен кадр с Destination Address={dest_addr}\n")

                    if (received_frame.source_address == 2 and fs_bits == '10010000'):
                        debug_texts.insert(INSERT, "Станция2: Кадр прошедший круг был прочитан\n")
                        if delete_marker == 0:
                            debug_texts.insert(INSERT, "Станция2: Запускаю новый(пустой) токен\n")
                            markToSend = Marker.Markers(SD=1, AC=0, ED=1)
                            markToSend = markToSend.packs()
                            Sender.is_marker_here = 0
                            Marker.send_Marker(Sender.second_connect, markToSend)
                        else:
                            debug_texts.insert(INSERT, "Станция2: Маркер удален\n")
                    else:
                        if dest_addr == 2:
                             fullpacket=received_frame
                             received_frame = convert_list_to_message(received_frame.data)

                             fullpacket.FS = 0b10010000  # утсановка что прочитано
                             frame_to_send = packSend.MyFrame(source_address=fullpacket.source_address, data=fullpacket.data,
                                                              dest_adress=fullpacket.destination_address, SD=0, AC=0b00010000, ED=0,
                                                              FS=fullpacket.FS)
                             stuffed_data = frame_to_send.packs()
                             packSend.send_frame(Sender.second_connect, stuffed_data)

                             txt2.insert(INSERT, received_frame)
                        else:
                            frame_to_send = packSend.MyFrame(source_address=received_frame.source_address, data=received_frame.data,
                                                             dest_adress=received_frame.destination_address,SD=0,AC=0b00010000,ED=0,FS=received_frame.FS)
                            stuffed_data = frame_to_send.packs()
                            sleep(1)
                            packSend.send_frame(Sender.second_connect, stuffed_data)
                else:
                    Sender.where_is_marker = 2
                    Sender.marker_event.set()
                    sleep(1)
                    if (Sender.is_marker_here == 0):
                        mark_received2.AC = Sender.markerInfo.AC
                        mark_received2 = mark_received2.packs()
                        if delete_marker == 0:
                            Marker.send_Marker(Sender.second_connect, mark_received2)
                            debug_texts.insert(INSERT, "Станция2: Получен пустой токен\n")
                        else:
                            debug_texts.insert(INSERT, "Станция2: Удален пустой токен\n")
            else:
                mark_received2.AC = Sender.markerInfo.AC
                mark_received2 = mark_received2.packs()
                if delete_marker == 0:
                    Marker.send_Marker(Sender.second_connect, mark_received2)
                debug_texts.insert(INSERT, "Станция2:  Приоритет станции ниже приоритета маркера\n")
    if choose_ports == 3:
        while 1:
            mark_received3 = Marker.receive_Marker(third_connect)

            Sender.markerInfo = mark_received3
            AC= mark_received3.AC.to_bytes(1, byteorder='little')
            AC = bytes_to_bits(AC)
            if Sender.priority==Sender.priority3:

                if AC[3] == '1':
                    Sender.where_is_marker = 3
                    received_frame = packSend.receive_frame(third_connect)

                    fs_bytes = received_frame.FS.to_bytes(1, byteorder='little')
                    fs_bits = bytes_to_bits(fs_bytes)

                    #print(f"FS={ fs_bits}")


                    dest_addr = received_frame.destination_address
                    debug_texts.insert(INSERT, f"Станция3: Получен кадр с Destination Address={dest_addr}\n")

                    if received_frame.source_address == 3 and fs_bits == '10010000':
                        debug_texts.insert(INSERT, "Станция3: Кадр прошедший круг был прочитан\n")
                        if delete_marker == 0:
                            debug_texts.insert(INSERT, "Станция3: Запускаю новый(пустой) токен\n")
                            markToSend = Marker.Markers(SD=1, AC=0, ED=1)
                            markToSend = markToSend.packs()
                            Sender.is_marker_here = 0
                            Marker.send_Marker(Sender.third_connect, markToSend)
                        else:
                            debug_texts.insert(INSERT, "Станция3:токен удален\n")
                    else:
                        if dest_addr==3:
                            fullpacket=received_frame
                            received_frame = convert_list_to_message(received_frame.data)

                            fullpacket.FS=0b10010000 #утсановка что прочитано
                            frame_to_send=packSend.MyFrame(source_address=fullpacket.source_address, data=fullpacket.data,
                                                             dest_adress=fullpacket.destination_address,SD=0,AC=0b00010000,ED=0,FS=fullpacket.FS)
                            stuffed_data = frame_to_send.packs()
                            packSend.send_frame(Sender.third_connect, stuffed_data)
                            txt3.insert(INSERT, received_frame)
                        else:
                            frame_to_send = packSend.MyFrame(source_address=received_frame.source_address, data=received_frame.data,
                                                             dest_adress=received_frame.destination_address,SD=0,AC=0b00010000,ED=0,FS=received_frame.FS)
                            sleep(1)
                            stuffed_data = frame_to_send.packs()
                            packSend.send_frame(Sender.third_connect, stuffed_data)
                else:
                    Sender.where_is_marker = 3
                    Sender.marker_event.set()
                    sleep(1)
                    if (Sender.is_marker_here == 0):
                        mark_received3.AC=Sender.markerInfo.AC
                        mark_received3 = mark_received3.packs()
                        if delete_marker == 0:
                            Marker.send_Marker(Sender.third_connect, mark_received3)
                            debug_texts.insert(INSERT, "Станция3: Получен пустой токен\n")
                        else:
                            debug_texts.insert(INSERT, "Станция3: Удален пустой токен\n")
            else:
                mark_received3.AC = Sender.markerInfo.AC
                mark_received3 = mark_received3.packs()
                if delete_marker == 0:
                    Marker.send_Marker(Sender.third_connect, mark_received3)

                debug_texts.insert(INSERT, "Станция3:  Приоритет станции ниже приоритета маркера\n")
def readfunc(text,number_station,debug_text):
    global txt1,txt2,txt3,debug_texts
    global choose_ports,counter
    debug_texts=debug_text
    choose_ports=number_station
    counter+=1
    if counter==1:
        txt1=text
    else:
        if counter == 2:
            txt2 = text
        else:
            if counter == 3:
                txt3 = text
    thread = threading.Thread(target=reads,daemon=True)
    thread.start()
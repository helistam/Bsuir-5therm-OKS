import random
import struct
import time
from tkinter import INSERT

import serial
from sostwin import Sost, print_time, print_collision

propagation_time = 1
transmission_time = propagation_time * 2
__try_counter = 0
class MyFrame:
    def __init__(self, source_address, data,fcs):
        self.source_address = source_address
        self.destination_address = 0
        self.flag = ord('z') + 3
        self.data = data
        self.fcs = fcs

    def packs(self):
        return struct.pack('<cBBBBBH', bytes([self.flag]),self.destination_address, self.source_address,
                           self.data[0], self.data[1], self.data[2], self.fcs)

    @staticmethod
    def unpack(data):
        source_address, destination_address, flag, data1, data2, data3, fcs = struct.unpack('<BBcBBBH', data)
        return MyFrame(source_address, [data1, data2, data3],fcs)


def send_frame(serial_port, frame):
    return serial_port.write(frame)

def receive_frame(serial_port):
    data = serial_port.read(8)  # Считываем 8 байт (размер кадра)
    if data.decode("windows-1251")=="11111111":
        print("collision")
        strtoencode="00000000"
        data=strtoencode.encode("windows-1251")
    Sost.readpacket = data
    print(f"Received Data: {data}")
    return MyFrame.unpack(data)


def send_jam(ser):
    jam_signal = "11111111"
    send_frame(ser,jam_signal.encode("windows-1251"))
    print("Jam signal")

def wait_transmission_time():
    print_time(transmission_time)
    time.sleep(transmission_time)

def increment_try_counter():
    global __try_counter
    __try_counter += 1
    print(f"Try counter is equal {__try_counter}")

def is_try_counter_max() -> bool:
    if __try_counter > 10:
        print("Error: Too many tries")
        return True
    return False

def calculate_and_wait_random_delay():
    time_to_wait = random.randint(0, 2 ** __try_counter)
    print(f"Generated time is {time_to_wait} (random from 0 to {2 ** __try_counter})")
    print(f"Waiting for {time_to_wait}s...")
    time.sleep(time_to_wait)

def clear_try_counter():
    __try_counter = 0

collision_probability = 0.25

def simulate_collision()-> bool:
    # Генерируем случайное число от 0 до 1
    random_number = random.random()

    if random_number <= collision_probability:
        # Произошла коллизия
        print_collision(1)
        return True
    else:
        print_collision(0)
        # Передача данных успешна
        print("Передача данных успешна")
        return False


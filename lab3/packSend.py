import struct
import serial
from sostwin import Sost
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
    Sost.readpacket = data
    print(f"Received Data: {data}")
    return MyFrame.unpack(data)



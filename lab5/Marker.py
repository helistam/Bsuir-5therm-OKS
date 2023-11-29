import struct
import serial
class Markers:
    def __init__(self, SD, AC,ED):
        self.SD = SD
        self.AC = AC
        self.ED =ED

    def packs(self):
        return struct.pack('<bbb',self.SD,self.AC,self.ED)

    @staticmethod
    def unpack(data):
        SD,AC,ED = struct.unpack('<bbb', data)
        return Markers(SD,AC,ED)

def send_Marker(serial_port, frame):
    return serial_port.write(frame)

def receive_Marker(serial_port):
    data = serial_port.read(3)  # Считываем 8 байт (размер кадра)
    return Markers.unpack(data)



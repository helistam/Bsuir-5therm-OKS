import struct
import serial
class MyFrame:
    def __init__(self, source_address, data,dest_adress,SD, AC,ED,FS):
        self.source_address = source_address    #SA
        self.destination_address = dest_adress  #DA
        self.RI = 0               #RI
        self.data = data
        self.fcs = 0
        self.ED=0
        self.FS=FS
        self.IFG=0
        self.SD = SD
        self.AC = AC
        self.ED = ED
    def packs(self):
        return struct.pack('<bbbbBBBBBHBBB', self.SD,self.AC,self.ED,self.RI,self.destination_address, self.source_address,
                           self.data[0], self.data[1], self.data[2], self.fcs,self.ED,self.FS,self.IFG)

    @staticmethod
    def unpack(data):
        flag, destination_address, source_address, data1, data2, data3, fcs,ED,FS,IFG = struct.unpack('<BBbBBBHBBB', data)
        return MyFrame(source_address, [data1, data2, data3],destination_address,0,0,0,FS)
def send_frame(serial_port, frame):
    return serial_port.write(frame)

def receive_frame(serial_port):
    data = serial_port.read(11)  # Считываем 8 байт (размер кадра)

    print(f"Received Data: {data}")
    return MyFrame.unpack(data)



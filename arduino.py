import serial
from time import sleep

class Arduino:
    def __init__(self, port, rate=19200, write_timeout=0.1):
        self.con = serial.Serial(port, baudrate=rate, write_timeout=write_timeout)
        sleep(1)
        
    def write(self, message):
        try:
            self.con.write(str(message).encode('utf-8'))
        except:
            pass
        
    def read(self):
        try:
            message = self.con.readline().decode('utf-8').strip()
            return self.con.readline().decode('utf-8').strip()
        except:
            return "Error"
            
    
    def query(self, message):
        self.write(message)
        return self.read()
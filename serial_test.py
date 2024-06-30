import serial
from time import sleep

step_delay = 0.5

con = serial.Serial("COM4", baudrate=19200)
sleep(2)

for i in range(0, 95, 5):
    con.write(str(i).encode('ascii'))
    sleep(step_delay)
    print(con.readline())
    print(con.readline())
    
for i in range(90, -5, -5):
    con.write(str(i).encode('ascii'))
    sleep(step_delay)
    print(con.readline())
    print(con.readline())
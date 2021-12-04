import serial
ser=serial.Serial("/dev/ttyUSB0",115200,timeout=0.01)
while True:
    number = str(ser.read(),"utf-8")
    if number == 'L':
        print('left')
    if number == 'R':
        print('Right')

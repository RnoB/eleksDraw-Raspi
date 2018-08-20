import serial
import time

s = []

def intializeDrawer():
    global s
    s = serial.Serial('/dev/ttyUSB0',115200)
    s.write("\r\n\r\n")
    time.sleep(2)
    s.flushInput()

def closeDrawer():

    s.close()

def penUp():
    s.flushInput()
    s.write(('M5S0'.strip()+'\r\n').encode('UTF-8'))
    s.readline()
    
def penDown():
    s.flushInput()
    s.write(('M3S30'.strip()+'\r\n').encode('UTF-8'))
    s.readline()

def main():
    intializeDrawer()
    penUp()
    penDown()
    penUp()
    penDown()
    penUp()
    penDown()
    closeDrawer()

if __name__ == "__main__":
    main()
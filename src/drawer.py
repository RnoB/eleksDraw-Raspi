import serial
import time
import math

s = []
x = 0
y = 0
def intializeDrawer():
    global s
    s = serial.Serial('/dev/ttyUSB0',115200)
    s.write("\r\n\r\n".encode('UTF-8'))
    time.sleep(2)
    s.flushInput()


def sendCommand(gCode):
    print(gCode)
    s.flushInput()
    s.write(gCode)
    out = s.readline()
    print(out)

def toPosition(x0,y0,speed = 3500):
    gCode = (('G1X'+str(x0)+'Y'+str(y0)+'F'+speed).strip()+'\r\n').encode('UTF-8')
    sendCommand(gCode)
    

def closeDrawer():
    toPosition(0,0)
    s.flushInput()
    s.write(('M30'.strip()+'\r\n').encode('UTF-8'))
    s.readline()
    s.close()

def penUp():
    s.flushInput()
    s.write(('M5S0'.strip()+'\r\n').encode('UTF-8'))
    s.readline()
    
def penDown():
    s.flushInput()
    s.write(('M3S30'.strip()+'\r\n').encode('UTF-8'))
    s.readline()

def line(x0,y0,length,angle):
    
    xf = x+L*math.cos(angle)


def main():
    intializeDrawer()
    penUp()
    penDown()
    penUp()
    penDown()
    penUp()
    penDown()
    penUp()
    closeDrawer()

if __name__ == "__main__":
    main()
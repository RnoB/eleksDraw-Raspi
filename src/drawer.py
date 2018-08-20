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
    sendCommand('G90\r\n'.encode('UTF-8')) # Set to Absolute Positioning
    sendCommand('G1Z0\r\n'.encode('UTF-8')) # linear movement no z position
    sendCommand('G21\r\n'.encode('UTF-8')) # G21 ; Set Units to Millimeters


def sendCommand(gCode):
    print(gCode)
    s.flushInput()
    s.write(gCode)
    out = s.readline()
    print(out)

def toPosition(x0,y0,speed = 3500):
    gCode = (('G1X'+str(x0)+'Y'+str(y0)+'F'+str(speed)).strip()+'\r\n').encode('UTF-8')
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

def line(x0,y0,length,angle=0,speed=2000):
    
    xf = x0+length*math.cos(angle)
    yf = y0+length*math.sin(angle)
    toPosition(x0,y0)
    penDown()
    toPosition(xf,yf)
    penUp()
    time.sleep(1)

def main():
    intializeDrawer()
    line(50,50,50,0)
    line(10,10,5,.1)
    line(10,10,5,.2)
    line(10,10,5,.4)
    line(10,10,5,.8)
    line(10,10,5,1.6)
    closeDrawer()

if __name__ == "__main__":
    main()
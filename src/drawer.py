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
    sendCommand(('M5S0'.strip()+'\r\n').encode('UTF-8'))


    
def penDown():

    sendCommand(('M3S30'.strip()+'\r\n').encode('UTF-8'))


def line(x0,y0,xf=-999,yf=-999,length=1,angle=0,speed=2000):
    
    xf = x0+length*math.cos(angle)
    yf = y0+length*math.sin(angle)
    toPosition(x0,y0)
    penDown()
    toPosition(xf,yf)
    penUp()

def square(xc,yc,R):
    toPosition(xc-R/2,yc-R/2)
    penDown()
    toPosition(xc+R/2,yc-R/2)
    toPosition(xc+R/2,yc+R/2)
    toPosition(xc-R,/2yc+R/2)
    toPosition(xc-R/2,yc-R/2)
    penUp()

def main():
    intializeDrawer()
    line(50,50,length=50,angle=0)
    line(50,50,length=55,angle=.1)
    line(50,50,length=60,angle=.2)
    line(50,50,length=65,angle=.4)
    line(50,50,length=70,angle=.8)
    line(50,50,length=75,angle=1.6)
    square(50,5)
    closeDrawer()

if __name__ == "__main__":
    main()
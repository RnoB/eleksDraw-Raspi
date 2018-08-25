import serial
import time
import math
import numpy as np
import random
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
    sendCommand('G1Z0F10\r\n'.encode('UTF-8')) # linear movement no z position
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

def noise(xMax):
    return xMax*random.random()


def line(x0,y0,xf=-999,yf=-999,length=1,angle=0,speed=2000):
    
    xf = x0+length*math.cos(angle)
    yf = y0+length*math.sin(angle)
    toPosition(x0,y0)
    penDown()
    toPosition(xf,yf)
    penUp()

def square(xc,yc,R,anisotropy = 1,angle=0,speed=2000,noise = 0):
    x = [-R/2,+R/2]
    y = [-anisotropy*R/2,+anisotropy*R/2]

    toPosition(xc+(x[0]*math.cos(angle)-y[0]*math.sin(angle))+noise(noise),yc+(x[0]*math.sin(angle)+y[0]*math.cos(angle))+noise(noise),speed=speed)
    penDown()
    toPosition(xc+(x[1]*math.cos(angle)-y[0]*math.sin(angle))+noise(noise),yc+(x[1]*math.sin(angle)+y[0]*math.cos(angle))+noise(noise),speed=speed)
    toPosition(xc+(x[1]*math.cos(angle)-y[1]*math.sin(angle))+noise(noise),yc+(x[1]*math.sin(angle)+y[1]*math.cos(angle))+noise(noise),speed=speed)
    toPosition(xc+(x[0]*math.cos(angle)-y[1]*math.sin(angle))+noise(noise),yc+(x[0]*math.sin(angle)+y[1]*math.cos(angle))+noise(noise),speed=speed)
    toPosition(xc+(x[0]*math.cos(angle)-y[0]*math.sin(angle))+noise(noise),yc+(x[0]*math.sin(angle)+y[0]*math.cos(angle))+noise(noise),speed=speed)
    penUp()

def main():
    intializeDrawer()
    try:
        #line(50,50,length=50,angle=0)
        #line(50,50,length=55,angle=.1)
        #line(50,50,length=60,angle=.2)
        #line(50,50,length=65,angle=.4)
        #line(50,50,length=70,angle=.8)
        #line(50,50,length=75,angle=1.6)
        for k in range(0,20):
            square(10,7,k/2.0,noise = .1)
            #for j in range(0,10):
                #square((k+1)*11,(j+1)*11,10,angle=math.pi*(k*j)/(400))
    except Exception as e: 
        print(e)
        toPosition(0,0)
    closeDrawer()

if __name__ == "__main__":
    main()
import serial
import time
import math
import numpy as np
import random
import sys
import os
import traceback
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

def toPositionCurved(x0,y0,R,cw=True,speed = 3500):
    if cw:
        gCommand = 'G2'
    else:
        gCommand = 'G3'
    gCode = ((gCommand+'X'+str(x0)+'Y'+str(y0)+'R'+str(R)+'F'+str(speed)).strip()+'\r\n').encode('UTF-8')
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

def noiser(xMax):
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
    xIdx = [1,1,0,0]
    yIdx = [0,1,1,0]
    xSquare = []
    for k in range(0,4):
        xSquare.append([xc+(x[xIdx[k]]*math.cos(angle)-y[yIdx[k]]*math.sin(angle))+noiser(noise),xc+(x[xIdx[k]]*math.sin(angle)+y[yIdx[k]]*math.cos(angle))+noiser(noise)])
    toPosition(xSquare[-1][0],xSquare[-1][1],speed=speed)
    penDown()
    for xs in xSquare:
        toPosition(xs[0],xs[1],speed=speed)
    penUp()

def circle(x,y,R,speed = 2000,cw = False):
    toPositionCurve(x-R,y,R,speed=speed)
    penDown()
    toPosition(x+R,y,R,speed=speed,cw=cw)
    toPosition(x-R,y,R,speed=speed,cw=cw)
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
        for k in range(0,10):
            #square(100,70,10*k/2.0,noise = 3)
            for j in range(0,10):
                #square((k+1)*11,(j+1)*11,10,angle=math.pi*(k*j)/(400))
                circle((k+1)*11,(j+1)*11,k+j)
    except Exception as e: 
        print(traceback.format_exc())
        toPosition(0,0)
    closeDrawer()

if __name__ == "__main__":
    main()
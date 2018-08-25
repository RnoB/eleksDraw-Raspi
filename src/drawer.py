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


def noiser(xMax):
    return xMax*random.random()



class Drawer:
    s = []
    def sendCommand(self,gCode):
        print(gCode)
        self.s.flushInput()
        self.s.write(gCode)
        out = self.s.readline()
        print(out)

    def toPosition(self,x0,y0,speed = 3500):
        gCode = (('G1X'+str(x0)+'Y'+str(y0)+'F'+str(speed)).strip()+'\r\n').encode('UTF-8')
        self.sendCommand(gCode)

    def toPositionCurved(self,x0,y0,R,cw=True,speed = 3500):
        if cw:
            gCommand = 'G2'
        else:
            gCommand = 'G3'
        gCode = ((gCommand+'X'+str(x0)+'Y'+str(y0)+'R'+str(R)+'F'+str(speed)).strip()+'\r\n').encode('UTF-8')
        self.sendCommand(gCode)


    def closeDrawer(self):
        self.toPosition(0,0)
        self.s.flushInput()
        self.s.write(('M30'.strip()+'\r\n').encode('UTF-8'))
        self.s.readline()
        self.s.close()

    def penUp(self):
        self.sendCommand(('M5S0'.strip()+'\r\n').encode('UTF-8'))
        
    def penDown(self):
        self.sendCommand(('M3S30'.strip()+'\r\n').encode('UTF-8'))

    def line(self,x0,y0,xf=-999,yf=-999,length=1,angle=0,speed=2000):
        
        xf = x0+length*math.cos(angle)
        yf = y0+length*math.sin(angle)
        self.toPosition(x0,y0)
        self.penDown()
        self.toPosition(xf,yf)
        self.penUp()

    def square(self,xc,yc,R,anisotropy = 1,angle=0,speed=2000,noise = 0):
        x = [-R/2,+R/2]
        y = [-anisotropy*R/2,+anisotropy*R/2]
        xIdx = [1,1,0,0]
        yIdx = [0,1,1,0]
        xSquare = []
        for k in range(0,4):
            xSquare.append([xc+(x[xIdx[k]]*math.cos(angle)-y[yIdx[k]]*math.sin(angle))+noiser(noise),xc+(x[xIdx[k]]*math.sin(angle)+y[yIdx[k]]*math.cos(angle))+noiser(noise)])
        self.toPosition(xSquare[-1][0],xSquare[-1][1],speed=speed)
        self.penDown()
        for xs in xSquare:
            self.toPosition(xs[0],xs[1],speed=speed)
        self.penUp()

    def circle(self,x,y,R,speed = 2000,cw = False):
        self.toPosition(x-R,y,speed=speed)
        self.penDown()
        self.toPositionCurved(x+R,y,R,speed=speed,cw=cw)
        self.toPositionCurved(x-R,y,R,speed=speed,cw=cw)
        self.penUp()



    def __init__(self):
        
        self.s = serial.Serial('/dev/ttyUSB0',115200)
        self.s.write("\r\n\r\n".encode('UTF-8'))
        time.sleep(2)
        self.s.flushInput()
        self.sendCommand('G90\r\n'.encode('UTF-8')) # Set to Absolute Positioning
        self.sendCommand('G1Z0F10\r\n'.encode('UTF-8')) # linear movement no z position
        self.sendCommand('G21\r\n'.encode('UTF-8')) # G21 ; Set Units to Millimeters




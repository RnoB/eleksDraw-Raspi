import serial
import time
import math
import numpy as np
import random
import sys
import os
import traceback
import drawNet
import drawIP
s = []
x = 0
y = 0


def noiser(xMax):
    return xMax*random.random()



class Drawer:
    s = []
    penPosition = True
    output = False
    def sendCommand(self,gCode):
        if self.output:
            print(gCode)
        self.s.flushInput()
        self.s.write(gCode)
        out = self.s.readline()
        if self.output:
            print(out)




    def toPosition(self,x0,y0,speed = 3500,polar = False):
        if polar:

            lL = np.sqrt((self.dx + x0)**2+(self.dy+y0)**2)-self.dist
            lR = np.sqrt((self.dx - x0)**2+(self.dy+y0)**2)-self.dist
            x0 = lL
            y0 = lR
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
        self.sendCommand(('M3S30'.strip()+'\r\n').encode('UTF-8'))
        self.penPosition=True 
        
    def penDown(self,):
        self.sendCommand(('M3S90'.strip()+'\r\n').encode('UTF-8'))
        self.penPosition=False

    def line(self,x0,y0,xf=-999,yf=-999,length=1,angle=0,speed=2000):
        
        xf = x0+length*math.cos(angle)
        yf = y0+length*math.sin(angle)
        self.toPosition(x0,y0)
        self.penDown()
        self.toPosition(xf,yf)
        self.penUp()

    def lines(self,x,y,speed=2000):
        self.toPosition(x[0],y[0])
        self.penDown()
        for k in range(0,len(x)):
            self.toPosition(x[k],y[k])
        self.penUp()



    def square(self,xc,yc,R,anisotropy = 1,angle=0,speed=2000,noise = 0):
        x = [-R,+R]
        y = [-anisotropy*R,+anisotropy*R]
        xIdx = [1,1,0,0]
        yIdx = [0,1,1,0]
        xSquare = []
        for k in range(0,4):
            xSquare.append([xc+(x[xIdx[k]]*math.cos(angle)-y[yIdx[k]]*math.sin(angle))+noiser(noise),yc+(x[xIdx[k]]*math.sin(angle)+y[yIdx[k]]*math.cos(angle))+noiser(noise)])
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



    def __init__(self,output = False,dx = 0,dy=0,de = 40):
        self.penPosition=False
        self.s = serial.Serial('/dev/ttyUSB0',115200)
        self.s.write("\r\n\r\n".encode('UTF-8'))
        time.sleep(2)
        self.s.flushInput()
        self.sendCommand('G90\r\n'.encode('UTF-8')) # Set to Absolute Positioning
        self.sendCommand('G1Z0F10\r\n'.encode('UTF-8')) # linear movement no z position
        self.sendCommand('G21\r\n'.encode('UTF-8')) # G21 ; Set Units to Millimeters
        self.output = output
        self.dx = dx
        self.dy = dy
        self.de = de
        self.dist = np.sqrt(dx**2+dy**2)


class DrawerNet:
    s = []
    penPosition = True
    output = False




    def toPosition(self,x0,y0,speed = 3500,polar = False):
        drawerNet.sendPosition(x0,y0)

    def toPositionCurved(self,x0,y0,R,cw=True,speed = 3500):
        pass


    def closeDrawer(self):
        pass


    def penUp(self):
        drawNet.pen("up")
        
    def penDown(self,):
        drawNet.pen("down")

    def line(self,x0,y0,xf=-999,yf=-999,length=1,angle=0,speed=2000):
        
        xf = x0+length*math.cos(angle)
        yf = y0+length*math.sin(angle)
        drawerNet.sendPosition(x0,y0)
        drawerNet.penDown()
        self.toPosition(xf,yf)
        self.penUp()

    def lines(self,x,y,speed=2000):
        drawNet.sendLines(x,y)



    def square(self,xc,yc,R,anisotropy = 1,angle=0,speed=2000,noise = 0):
        pass

    def circle(self,x,y,R,speed = 2000,cw = False):
        pass



    def __init__(self):
        pass






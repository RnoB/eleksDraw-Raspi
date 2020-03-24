import serial
import time
import math
import numpy as np
import random
import sys
import os
import traceback
try:
    from drawer import drawNet
    from drawer import drawIP
except:
    pass
try:
    import drawNet
    import drawIP
except:
    pass
s = []
x = 0
y = 0

penMove = 'M3S'
penUpCode = 30
penDownCode = 90





def noiser(xMax):
    return xMax*random.random()



class Drawer:
    s = []
    penPosition = True
    output = False
    penCode = [penUpCode,penDownCode]
    penCodeSmooth = []
    def sendCommand(self,gCode):
        if self.output:
            print(gCode)
        self.s.flushInput()
        self.s.write(gCode)
        out = self.s.readline()
        if self.output:
            print(out)


    def penInvert(self,invert = True):
        codeSmooth = np.arange(self.penCode[0]+1,self.penCode[1]+1,5)
        if invert:
            self.penCode = [penDownCode,penUpCode]
            self.penCodeSmooth.append((codeSmooth))
            self.penCodeSmooth.append((np.flip(codeSmooth)))

        else:
            self.penCode = [penUpCode,penDownCode]
            self.penCodeSmooth.append((np.flip(codeSmooth)))
            self.penCodeSmooth.append((codeSmooth))

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

    def penUp(self,smooth = False):
        if not smooth:
            self.sendCommand(((penMove+str(self.penCode[0])).strip()+'\r\n').encode('UTF-8'))

        else:
            

            for code in self.penCodeSmooth[0]:
                self.sendCommand(((penMove+str(code)).strip()+'\r\n').encode('UTF-8'))
                time.sleep(.05)
        self.penPosition=True 
        
    def penDown(self,smooth = False):
        if not smooth:
            self.sendCommand(((penMove+str(self.penCode[1])).strip()+'\r\n').encode('UTF-8'))
        else:
            penCodes = np.arange(self.penCode[0]+1,self.penCode[1]+1,5)
            for code in self.penCodeSmooth[1]:   
                self.sendCommand(((penMove+str(code)).strip()+'\r\n').encode('UTF-8'))
                time.sleep(.05)
        self.penPosition=False

    def line(self,x0,y0,xf=-999,yf=-999,length=1,angle=0,speed=2000,xOffset=0,yOffset=0,polar=False,smooth = False):
        
        xf = x0+length*math.cos(angle)+xOffset
        yf = y0+length*math.sin(angle)+yOffset
        self.toPosition(x0,y0)
        self.penDown(smooth = smooth)
        self.toPosition(xf,yf,speed)
        self.penUp(smooth = smooth)

    def lines(self,x,y,xOffset=0,yOffset=0,speed=2000,polar=False,smooth=False):
        self.toPosition(x[0]+xOffset,y[0]+yOffset,polar=polar,speed=2*speed)
        self.penDown(smooth = smooth)
        k0=0
        try:
            for k in range(0,len(x)):
                k0 = k
                
                self.toPosition(x[k]+xOffset,y[k]+yOffset,polar=polar,speed=speed)
        except:
            print('--- CRASH !!!! ---')
            print("length : "+str(len(x)))
            print("  k0   : "+str(k0))
        self.penUp(smooth = smooth)



    def square(self,xc,yc,R,anisotropy = 1,angle=0,speed=2000,noise = 0,polar=False):
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


    def squareCorner(self,x0,y0,x1,y1,noise = 0,polar=False,xOffset=0,yOffset=0):
        x = [x0,x1]
        y = [y0,y1]
        xIdx = [1,1,0,0]
        yIdx = [0,1,1,0]
        xSquare = []
        for k in range(0,4):
            xSquare.append([x[xIdx[k]]+noiser(noise),y[yIdx[k]]+noiser(noise)])
        self.toPosition(xSquare[-1][0],xSquare[-1][1],polar=polar)
        self.penDown()
        for xs in xSquare:
            self.toPosition(xs[0]+xOffset,xs[1]+yOffset)
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
        drawNet.sendPosition(x0,y0)

    def toPositionCurved(self,x0,y0,R,cw=True,speed = 3500):
        pass


    def closeDrawer(self):
        drawNet.sendPosition(0,0)


    def penUp(self):
        drawNet.pen("up")
        
    def penDown(self,):
        drawNet.pen("down")

    def line(self,x0,y0,xf=-999,yf=-999,xOffset=0,yOffset=0,length=1,angle=0,speed=2000):
        
        xf = x0+length*math.cos(angle)+xOffset
        yf = y0+length*math.sin(angle)+yOffset
        drawNet.sendPosition(x0,y0)
        drawNet.penDown()
        self.toPosition(xf,yf)
        self.penUp()

    def lines(self,x,y,speed=2000):
        drawNet.sendLines(x,y)



    def square(self,xc,yc,R,anisotropy = 1,angle=0,speed=2000,noise = 0):
        x = [-R,+R]
        y = [-anisotropy*R,+anisotropy*R]
        xIdx = [1,1,0,0]
        yIdx = [0,1,1,0]
        xSquare = []
        for k in range(0,4):
            xSquare.append([xc+(x[xIdx[k]]*math.cos(angle)-y[yIdx[k]]*math.sin(angle))+noiser(noise),yc+(x[xIdx[k]]*math.sin(angle)+y[yIdx[k]]*math.cos(angle))+noiser(noise)])
        self.toPosition(xSquare[-1][0],xSquare[-1][1])
        self.penDown()
        for xs in xSquare:
            self.toPosition(xs[0],xs[1])
        self.penUp()

    def squareCorner(self,x0,y0,x1,y1,noise = 0):
        x = [x0,x1]
        y = [y0,y1]
        xIdx = [1,1,0,0]
        yIdx = [0,1,1,0]
        xSquare = []
        for k in range(0,4):
            xSquare.append([x[xIdx[k]]+noiser(noise),y[yIdx[k]]+noiser(noise)])
        self.toPosition(xSquare[-1][0],xSquare[-1][1])
        self.penDown()
        for xs in xSquare:
            self.toPosition(xs[0],xs[1])
        self.penUp()

    def circle(self,x,y,R,speed = 2000,cw = False):
        pass



    def __init__(self):
        pass






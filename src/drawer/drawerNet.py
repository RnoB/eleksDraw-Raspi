import serial
import time
import math
import numpy as np
import random
import sys
import os
import traceback
import drawer
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




    def toPosition(self,x0,y0,speed = 3500,polar = False):
        drawNet.sendPosition(x0,y0)

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
        drawNet.sendPosition(x0,y0)
        drawNet.penDown()
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






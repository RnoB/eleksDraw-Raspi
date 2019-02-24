
from drawer import drawer
import traceback
import colorsys
from blinkt import set_pixel, set_brightness, show, clear
import numpy as np
import random
import math
from kinecter import kinecter
import time
running = True

from blinked import blinked


def switchColor(col):
    #clear()
    if col == 0:
        for k in range(0,2):
            set_pixel(k,0,255,0)
    if col == 1:
        for k in range(0,2):
            set_pixel(k,255,0,0)
    if col == 2:
        for k in range(0,2):
            set_pixel(k,0,0,255)
    show()

def animColor():

    spacing = 360.0 / 16.0
    hue = 0
    clear()
    hue = int(time.time() * 100) % 360
    for x in range(8):

        offset = x * spacing
        h = ((hue + offset) % 360) / 360.0
        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
        set_pixel(x, r, g, b)

        time.sleep(.05)
        show()

    time.sleep(2)
    clear()
    show()




def scaler(x,y,scale=100,offsetX = 5,offsetY = 5,invert=False):
    if invert:
        x2 = np.int(480*(x-offsetX)/scale)
        y2 = np.int(480*(y-offsetY)/scale)
    else:
        x2 = scale*x/480+offsetX
        y2 = scale*y/480+offsetY

    return x2,y2


def round(x, base=1):
    return base * np.round(x/base)


def main():
    set_brightness(.05)
    blinked.switchColor('g',[0])
    try:
        kinect = kinecter.kinect()
        blinked.switchColor('o',[1])
        kinect.start()
        kinect.backGroundSubstractor(nFrames=50)
        kinect.stop()
        blinked.switchColor('p',[1])
        time.sleep(20)
        kinect.start()
        kinect.getDepthFrames(nFrames = 30,delay=.01,maxDepth=2049)
        kinect.stop()
        blinked.switchColor('c',[1])
        kinect.backgroundSubstract(blur=True,level=20)
        dX,dY,angle,angleZ = kinect.derivateFrames()
    except Exception as e: 
        print(traceback.format_exc())
 

    draw = drawer.Drawer(output = False)    
    z = kinect.frames[6]
    A = angle[6]
    idx = [6,7,8]
    nLines = 300
    size = 0
    X = []
    X2 = []
    scale = 110
    xu,yu = scaler(1,1,scale=scale,offsetX=0,offsetY=0)
    offsetA=[[-np.pi/3,0,np.pi/3],[-2*np.pi/3,np.pi,2*np.pi/3]]    
    blinked.switchColor('a',[0])
    blinked.switchColor('g',[1])
    rounder = 1.1
    speed = 2*rounder


    nx = 5

    rounder2 = 3*rounder
    if speed<rounder:
        speed = rounder

    try:
        for j in range(0,5):
            X3 = []
            X = []
            blinked.progressColor(j/5,'v','y',[4])
            nLines = 400#75*(3*l+j+1)
            kFrames = j+12
            z =kinect.frames[kFrames]
            A = angle[kFrames]
            AZ = angleZ[kFrames]
            #dist = random.uniform((j-nx*math.floor(j/nx)),1+(j-nx*math.floor(j/nx)))*5
            #
            dist = j*35
            offsetX = 5+math.floor(j/nx)*8+random.uniform(-1,1)
            offsetY = 5+dist
            print('offset : ' + str((offsetX,offsetY)))
            #offsetY = 5+j*27
            #offsetX = 5
            rounder = .2
            speed = 2*rounder


            rounder2 = 10*rounder
            if speed<rounder:
                speed = rounder
            for k in range(0,nLines):
                blinked.progressColor(k/nLines,'v','y',[5])
                size = 0
                trial =0
                while(size == 0):
                    trial+=1 
                    xLines = []
                    yLines = []

                    size = 0
                    xChecking = True
                    while xChecking:
                        kx = random.randint(0, 639)
                        ky = random.randint(0, 479)
                        x,y = scaler(kx,ky,scale=scale,offsetX=offsetX,offsetY=offsetY)
                        x = round(x+(.5-random.random())*xu,rounder/2.0)
                        y = round(y+(.5-random.random())*yu,rounder/2.0)
                        x2 = round(x,rounder2)
                        y2 = round(y,rounder2)
                        zTest = z[ky,kx]
                        Atest = A[ky,kx]
                        if (x2,y2) not in X2:
                            xChecking = False
                    running = True
                    if np.isnan(zTest) or np.isnan(Atest):
                        running=False
                    while running:
                        #print('x  : '+str((x,y)))
                        #print('k  : '+str((kx,ky)))
                        xLines.append(y)
                        yLines.append(x)
                        X.append((x,y))
                        X3.append((x2,y2))
                        speedZ = speed*np.cos(AZ[ky,kx])**.2
                        dx = round(x+speedZ*np.cos(A[ky,kx]),rounder)
                        dy = round(y+speedZ*np.sin(A[ky,kx]),rounder)
                        dx2 = round(x+speedZ*np.cos(A[ky,kx]),rounder2)
                        dy2 = round(y+speedZ*np.sin(A[ky,kx]),rounder2)
                        
                        dxk,dyk = scaler(dx,dy,scale=scale,offsetX=offsetX,offsetY=offsetY,invert=True)
                        
                        if (dxk>-1) and (dxk<640) and (dyk>-1) and (dyk<480) and size < 100 and (dx,dy) not in X and (dx2,dy2) not in X2:
                            x=dx
                            y=dy
                            kx=dxk
                            ky=dyk
                            zTest = z[ky,kx]
                            Atest = A[ky,kx]
                            AZtest = AZ[ky,kx]
                            size +=speedZ
                            if np.isnan(zTest) or np.isnan(Atest)or np.isnan(AZtest):
                                running=False
                        else:
                            running = False
                    if trial>100 and size==0:
                        size = -1
                if size>0:
                    print('new Line : '+str(k))
                    draw.lines(xLines,yLines)
            for x3 in X3:
                if x3 not in X2:
                    X2.append(x3)
                    if len(X2)>10000000:
                        del X2[0]
        #line(50,50,length=50,angle=0)
        #line(50,50,length=55,angle=.1)
        #line(50,50,length=60,angle=.2)
        #line(50,50,length=65,angle=.4)
        #line(50,50,length=70,angle=.8)
        #line(50,50,length=75,angle=1.6)
        #for k in range(0,10):
            #draw.square(100,70,10*k/2.0,noise = 3,speed=500)
            #for j in range(0,10):
                #square((k+1)*11,(j+1)*11,10,angle=math.pi*(k*j)/(400))
                #draw.circle((k+1)*11,(j+1)*11,k+j)
    except Exception as e: 
        print(traceback.format_exc())
        draw.toPosition(0,0)
    draw.closeDrawer()    
    switchColor(1)

if __name__ == "__main__":
    main()


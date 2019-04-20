
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

def spacer(depth,nx0):
    scale = 220
    heightMax=200
    nx = 10
    nx0=np.int(nx0)
    offsetY0 = []
    while heightMax>160:
        sizeImage = []
        offset = []
        for k in range(0,nx):
            Ht = np.sum(np.isnan(depth[nx0+k]),axis=0)!=480
            H = np.nonzero(Ht)
            Wt = np.sum(np.isnan(depth[nx0+k]),axis=1)!=640
            W = np.nonzero(Wt)
            sizeImage.append(scaler(W[0][-1]-W[0][0],H[0][-1]-H[0][0],scale=scale,offsetX = 0,offsetY = 0))
            offset.append(scaler(W[0][0],H[0][0],scale=scale,offsetX = 0,offsetY = 0))
            offsetY0.append(offset[-1][1])

        offsetX = offset[0][0]
        offsetY = np.min(offsetY0)
        heightMax = np.max(sizeImage,axis = 0)[1]
        scale=scale-5
    width = np.mean(sizeImage,axis = 0)[0]
    nx = np.int(round((1+random.random())*240/width))
    dist = (240-sizeImage[nx-1][0])/nx
    #dist = dist - ((dist*(nx-1)+sizeImage[nx-1][0])-240)/(nx-1)
    return scale,nx,dist,offsetX,offsetY


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


def drawing(kFrames,frames,angle,angleZ,draw,nLines = 400,scale = 70,A0=0,rounder=.1,noise = 0,offsetX = 0,offsetY=0,X2 = []):
    kFrames = np.int(kFrames)
    X3 = []
    X = []


    
    z = frames[kFrames]
    A = angle[kFrames]+A0
    AZ = angleZ[kFrames]

    
    speed = 2*rounder
    
    xL = []
    yL = []
    rounder2 = 3*rounder
    xu,yu = scaler(1,1,scale=scale,offsetX=0,offsetY=0)

    if speed<rounder:
        speed = rounder
    for k in range(0,nLines):

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
                xLines.append(y)
                yLines.append(x)
                X.append((x,y))
                X3.append((x2,y2))
                speedZ = speed#*np.cos(AZ[ky,kx])**.2
                angleD = A[ky,kx]+noise*(.5-random.random())
                dx = round(x+speedZ*np.cos(angleD),rounder)
                dy = round(y+speedZ*np.sin(angleD),rounder)
                dx2 = round(x+speedZ*np.cos(angleD),rounder2)
                dy2 = round(y+speedZ*np.sin(angleD),rounder2)
                dxk,dyk = scaler(dx,dy,scale=scale,offsetX=offsetX,offsetY=offsetY,invert=True)

                if (dxk > -1) and (dxk < 640) \
                and (dyk > -1) and (dyk < 480) \
                and size < 100 \
                and (dx,dy) not in X and (dx2,dy2) not in X2 \
                and AZ[ky,kx]-A0<1.5 \
                and dx < 170 and dy < 250 :
                    
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
            draw.lines(xLines,yLines)
    for x3 in X3:
        if x3 not in X2:
            X2.append(x3)
            if len(X2)>10000000:
                del X2[0]
    return X2



def main():
    set_brightness(.05)
    blinked.switchColor('g',[0])
    try:
        kinect = kinecter.kinect()
        blinked.switchColor('o',[1])
        kinect.start()
        kinect.backGroundSubstractor(nFrames=100)
        kinect.stop()
        blinked.switchColor('p',[1])
        time.sleep(20)
        kinect.start()
        kinect.getDepthFrames(nFrames = 30,delay=.01,maxDepth=2046)
        kinect.stop()
        blinked.switchColor('c',[1])
        kinect.backgroundSubstract(blur=True,level=10)
        dX,dY,angle,angleZ = kinect.derivateFrames()
    except Exception as e: 
        print(traceback.format_exc())
 

    draw = drawer.Drawer(output = False)    

    nLines = 600
    size = 0
    X = []
    X2 = []
    nx0=np.int(len(kinect.frames)/2)
    scale,nx,dist,offsetX,offsetY =  spacer(kinect.frames,nx0)
    print("scale : "+str(scale))
    print("n     : "+str(nx))
    print("offsetX  : "+str(offsetX))
    print("offsetY : "+str(offsetY))
    xu,yu = scaler(1,1,scale=scale,offsetX=0,offsetY=0)
    offsetA=[[-np.pi/3,0,np.pi/3],[-2*np.pi/3,np.pi,2*np.pi/3]]    
    blinked.switchColor('a',[0])
    blinked.switchColor('g',[1])
    rounder = 1.0
    speed = 2*rounder


    offsetX0 = 5-offsetY
    offsetY0 = 5-offsetX

    rounder2 = 3*rounder
    if speed<rounder:
        speed = rounder

    try:
        for j in range(0,nx):
            X3 = []
            X = []
            blinked.progressColor(j/5,'v','y',[4])
            
            kFrames = j+nx0
            #dist = random.uniform((j-nx*math.floor(j/nx)),1+(j-nx*math.floor(j/nx)))*5
            #
            
            offsetX = offsetX0
            offsetY = offsetY0+j*dist


            drawing(kFrames,kinect.frames,angle,angleZ,draw,nLines = nLines,scale = scale,A0=0,rounder=rounder,noise = 0.5,offsetX = offsetX,offsetY=offsetY,X2 = X2)
            

    except Exception as e: 
        print(traceback.format_exc())
        draw.toPosition(0,0)
    draw.closeDrawer()    
    switchColor(1)

if __name__ == "__main__":
    main()


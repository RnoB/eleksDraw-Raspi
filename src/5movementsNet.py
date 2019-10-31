
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

widthPaper = 240
heightPaper = 160
#widthPaper = 148
#heightPaper = 105

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

def spacer(depth,nx0,nx=20):
    scale = 220
    heightMax=200
    
    nx0=np.int(nx0)
    offsetY0 = []
    while heightMax>heightPaper-10:
        scale=scale-5
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
    width = np.mean(sizeImage,axis = 0)[0]
    nx = np.int(round((.8+1*random.random())*widthPaper/width))
    print(sizeImage)
    dist = ((widthPaper-10)-sizeImage[nx-1][0]+offset[0][0]-offset[nx-1][0])/(nx-1)
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


def drawing(kFrames,frames,angle,angleZ,draw,
            nLines = 400,scale = 70,A0=0,
            resolution=.1,speed = .4,distanceLine=.8 ,distanceFigure = 5.0,
            noise = 0,offsetX = 0,offsetY=0,figurePosition = []):
    kFrames = np.int(kFrames)

    imagePosition = []
    repetitionPosition = []

    
    z = frames[kFrames]
    A = angle[kFrames]+A0
    AZ = angleZ[kFrames]

    

    
    xL = []
    yL = []

    xu,yu = scaler(1,1,scale=scale,offsetX=0,offsetY=0)

    #if speed<distanceLine:
        #speed = distanceLine
    for k in range(0,nLines):

        size = 0
        trial =0
        while(size == 0):
            linePosition = []
            trial+=1 
            xLines = []
            yLines = []

            size = 0
            xChecking = True
            while xChecking:
                kx0 = random.randint(0, 639)
                ky0 = random.randint(0, 479)
                x,y = scaler(kx0,ky0,scale=scale,offsetX=offsetX,offsetY=offsetY)
                x0 = round(x+(.5-random.random())*xu,resolution/2.0)
                y0 = round(y+(.5-random.random())*yu,resolution/2.0)
                x = x0
                y = y0
                kx = kx0
                ky = ky0
                x1 = round(x,distanceLine)
                y1 = round(y,distanceLine)
                x2 = round(x,distanceFigure)
                y2 = round(y,distanceFigure)
                zTest = z[ky,kx]
                Atest = A[ky,kx]
                if (x2,y2) not in figurePosition and (x1,y1) not in imagePosition:
                    xChecking = False
            running = True
            if np.isnan(zTest) or np.isnan(Atest):
                running=False
            else:    
                while running:
                    xLines.append(y)
                    yLines.append(x)
                    linePosition.append((round(x,resolution),round(y,resolution)))
                    speedZ = speed#*np.cos(AZ[ky,kx])**.2
                    angleD = A[ky,kx]+noise*(.5-random.random())
                    dxS = x+speedZ*np.cos(angleD)
                    dyS = y+speedZ*np.sin(angleD)
                    dx = round(dxS,resolution)
                    dy = round(dyS,resolution)
                    dx1 = round(dx,distanceLine)
                    dy1 = round(dy,distanceLine)
                    dx2 = round(dx,distanceFigure)
                    dy2 = round(dy,distanceFigure)
                    dxk,dyk = scaler(dx,dy,scale=scale,offsetX=offsetX,offsetY=offsetY,invert=True)

                    if (dxk > -1) and (dxk < 640) \
                    and (dyk > -1) and (dyk < 480) \
                    and size < 100 \
                    and (dx,dy) not in linePosition\
                    and (dx1,dy1) not in imagePosition \
                    and (dx2,dy2) not in figurePosition \
                    and AZ[ky,kx]-A0<1.5 \
                    and dx < 170 and dy < 250 \
                    and dx > 0 and dy > 0:
                        
                        x=dxS
                        y=dyS
                        
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
                running = True
                
                x = x0
                y = y0
                kx = kx0
                ky = ky0     
                while running:
                    linePosition.append((round(x,resolution),round(y,resolution)))
                    speedZ = speed#*np.cos(AZ[ky,kx])**.2
                    angleD = np.pi+A[ky,kx]+noise*(.5-random.random())
                    dxS = x+speedZ*np.cos(angleD)
                    dyS = y+speedZ*np.sin(angleD)
                    dx = round(dxS,resolution)
                    dy = round(dyS,resolution)
                    dx1 = round(dx,distanceLine)
                    dy1 = round(dy,distanceLine)
                    dx2 = round(dx,distanceFigure)
                    dy2 = round(dy,distanceFigure)
                    dxk,dyk = scaler(dx,dy,scale=scale,offsetX=offsetX,offsetY=offsetY,invert=True)

                    if (dxk > -1) and (dxk < 640) \
                    and (dyk > -1) and (dyk < 480) \
                    and size < 100 \
                    and (dx,dy) not in linePosition\
                    and (dx1,dy1) not in imagePosition \
                    and (dx2,dy2) not in figurePosition \
                    and AZ[ky,kx]-A0<1.5 \
                    and dx < 170 and dy < 250 \
                    and dx > 0 and dy > 0:
                        
                        x=dxS
                        y=dyS
                        
                        kx=dxk
                        ky=dyk
                        zTest = z[ky,kx]
                        Atest = A[ky,kx]
                        AZtest = AZ[ky,kx]
                        size +=speedZ
                        if np.isnan(zTest) or np.isnan(Atest)or np.isnan(AZtest):
                            running=False
                        else:

                           xLines.insert(0,y)
                           yLines.insert(0,x)
                    else:
                        running = False
            if trial>100 and size==0:
                size = -1
        if size>0:
            #print("X : "+str(np.min(xLines))+" Y : "+str(np.min(yLines)))
            xLines = xLines[np.int(np.floor(.1*len(xLines))):0]
            yLines = yLines[np.int(np.floor(.1*len(xLines))):0]
            draw.lines(xLines,yLines)
            for position in linePosition:
                imagePosition.append((round(position[0],distanceLine),round(position[1],distanceLine)))
                repetitionPosition.append((round(position[0],distanceFigure),round(position[1],distanceFigure)))

    for position in repetitionPosition:
        if position not in figurePosition:
            figurePosition.append(position)
            if len(figurePosition)>10000000:
                del figurePosition[0]
    return figurePosition



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
        kinect.getDepthFrames(nFrames = 40,delay=.01,maxDepth=2049)
        kinect.stop()
        blinked.switchColor('c',[1])
        kinect.backgroundSubstract(blur=True,level=15)
        dX,dY,angle,angleZ = kinect.derivateFrames()
    except Exception as e: 
        print(traceback.format_exc())
 

    draw = drawer.DrawerNet()    
    draw.penUp()
    draw.squareCorner(0,0,widthPaper,heightPaper)
    nLines = 400
    size = 0

    X2 = []
    nx0=np.int(len(kinect.frames)/2)
    scale,nx,dist,offsetX,offsetY =  spacer(kinect.frames,nx0-1,nx0)
    print("scale : "+str(scale))
    print("n     : "+str(nx))
    print("offsetX  : "+str(offsetX))
    print("offsetY : "+str(offsetY))
    print("dist : "+str(dist))
    xu,yu = scaler(1,1,scale=scale,offsetX=0,offsetY=0)
    offsetA=[[-np.pi/3,0,np.pi/3],[-2*np.pi/3,np.pi,2*np.pi/3]]    
    blinked.switchColor('a',[0])
    blinked.switchColor('g',[1])




    offsetX0 = 5-offsetY
    offsetY0 = 5-offsetX



    d = np.linspace(.1,4,nx)
    nL = np.linspace(250,600,nx)

    sp = np.linspace(.2,4.0,nx)


    try:
        for j in range(0,nx):

            blinked.progressColor(j/nx,'v','y',[4])
            
            kFrames = j+nx0
            #dist = random.uniform((j-nx*math.floor(j/nx)),1+(j-nx*math.floor(j/nx)))*5
            #
            
            offsetX = 5-offsetX0
            offsetY = 5-offsetY0+j*dist

            #print("offset : "+str((offsetX,offsetY)))
            X2 = drawing(kFrames,kinect.frames,angle,angleZ,draw,nLines = 200,scale = scale,A0=0,\
                    offsetX = offsetX,offsetY=offsetY,figurePosition = X2,distanceLine = .6  ,speed = .2)
            

    except Exception as e: 
        print(traceback.format_exc())
        draw.toPosition(0,0)
    draw.closeDrawer()    
    switchColor(1)

if __name__ == "__main__":
    main()


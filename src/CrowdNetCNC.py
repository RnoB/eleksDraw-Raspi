
from drawer import drawer
import traceback
import colorsys
from blinkt import set_pixel, set_brightness, show, clear
import numpy as np
import random
import math
from kinecter import kinecter
import time
import asyncio
from evdev import InputDevice, categorize, ecodes
import threading
import glob
import os
import json
import pickle

running = True

widthPaper = 950
heightPaper = 950
#widthPaper = 148
#heightPaper = 105

from blinked import blinked

backgroundSub = False
drawLoop = False
pause = False
save = False

savePath = "/home/pi/save/"


def saveState(k0,j0,nL,scale,A0,X2,d1,d2,speed,crop,noise,dist,nx,ny):
    data = {'k0':k0,'j0':j0,'nL':nL,'scale':scale,'A0':A0,"X2":X2,"d1":d1,"d2":d2,"speed":speed,"crop":crop,"noise":noise,"dist":dist,"nx":nx,"ny":ny}

    with open(savePath+"parameters.p", 'wb') as fp:
        pickle.dump(data,fp, protocol=pickle.HIGHEST_PROTOCOL)


    
def saveFrames(frames,angle,angleZ,offset):
    data = {"frames":frames,"angle":angle,"angleZ":angleZ,"offset":offset}
    with open(savePath+"frames.p", 'wb') as fp:
        pickle.dump(data,fp,protocol=pickle.HIGHEST_PROTOCOL)
    
    
def loadState():
    with open(savePath+"parameters.json", 'rb') as fp:
        data = json.load(fp)
    return data['k0'],data['j0'],data['nL'],data['scale'],data['A0'],data['X2'],data['d1'],data['d2'],data['speed'],data['crop'],data['noise'],data['dist'],data['nx'],data['ny']

def loadFrames():
    with open(savePath+"frames.json", 'rb') as fp:
        data = json.load(fp)
    return data['frames'],data['angle'],data['angleZ']
    
    
def mouseListener():
    global backgroundSub
    global drawLoop
    global pause
    global colorK
    pressed = False
    dev = InputDevice('/dev/input/event0')
    for ev in dev.read_loop():
        
        if ev.type == 1:
            if ev.code == 272:
                backgroundSub = True
                pressed = not pressed
                if pressed and pause:
                
                    colorK +=1
                    colorK = colorK%3
                    #colorsChosen()
                if pause:
                    save = True
            elif ev.code ==273:
                drawLoop = True
                pressed = not pressed
                if pressed and pause:
                    colorK -=1
                    colorK = colorK%3
                    #colorsChosen()

            elif ev.code ==274:
                pressed = not pressed
                if pressed:
                    pause = not pause
                    print(pause)


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

def spacer(depth):

    ny = 10
    nx = 40
    overlap = 0.3

    heightReal = heightPaper / (1+((1-overlap)*(ny-1)))
    widths = []
    heights = []
    offsets = []
    for image in depth:
        Ht = np.sum(np.isnan(image),axis=0)!=480
        H = np.nonzero(Ht)
        Wt = np.sum(np.isnan(image),axis=1)!=640
        W = np.nonzero(Wt)
        offsets.append([-W[0][0],-H[0][0]])
        widths.append(W[0][-1]-W[0][0])
        heights.append(H[0][-1]-H[0][0])
    print(widths)
    print(heights)
    heightMax = np.mean(heights)
    widthMax = np.mean(widths)
    scale = getScale(heightMax,heightReal)
    sizeReal = scaler(widthMax,heightMax,scale,0,0)
    print("Max Size : "+str(sizeReal))
    nx = np.int(round(widthPaper/(sizeReal[0])))
    offset = []

    for k in range(0,len(offsets)):
        offset.append(scaler(offsets[k][0],offsets[k][1],scale=scale,offsetX = 0,offsetY = 0))
    dist = [1.0*(widthPaper-sizeReal[0])/nx,(1-overlap)*heightReal]
    
   
    #dist = dist - ((dist*(nx-1)+sizeImage[nx-1][0])-240)/(nx-1)
    return scale,nx,ny,dist,offset


def scaler(x,y,scale=100,offsetX = 5,offsetY = 5,invert=False):
    if invert:
        x2 = np.int(480*(x-offsetX)/scale)
        y2 = np.int(480*(y-offsetY)/scale)
    else:
        x2 = scale*x/480+offsetX
        y2 = scale*y/480+offsetY

    return x2,y2

def getScale(wPixel,wPaper):
    return 480*wPaper/wPixel



def round(x, base=1):
    return base * np.round(x/base)


def drawing(kFrames,frames,angle,angleZ,draw,
            nLines = 400,scale = 70,A0=0,
            resolution=.1,speed = .4,distanceLine=.8 ,distanceFigure = 5.0,
            noise = 0,offsetX = 0,offsetY=0,figurePosition = [],cropFactor = .3,reverse=True):
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
        while(pause):
            time.sleep(1)

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
                    and size < 200 \
                    and (dx,dy) not in linePosition\
                    and (dx1,dy1) not in imagePosition \
                    and (dx2,dy2) not in figurePosition \
                    and dx < heightPaper and dy < widthPaper \
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

                if reverse:
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
                        and size < 200 \
                        and (dx,dy) not in linePosition\
                        and (dx1,dy1) not in imagePosition \
                        and (dx2,dy2) not in figurePosition \
                        and dx < heightPaper and dy < widthPaper \
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
            xLines = xLines[np.int(np.floor(cropFactor*len(xLines))):]
            yLines = yLines[np.int(np.floor(cropFactor*len(xLines))):]
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
    mouseThread = threading.Thread(target = mouseListener)
    mouseThread.daemon = True
    mouseThread.start()

    draw = drawer.DrawerNet(2)

    draw.penUp()
    draw.toPosition(0,0)
    set_brightness(.05)
    blinked.switchColor('g',[0])
    
    k0 = 0
    j0 = 0
    while(not backgroundSub):
        time.sleep(.1)
    if os.path.isfile(savePath+"parameters.txt"):
        dist = [0,0]
        k0,j0,nL,scale,A0,X2,d1,d2,speed,crop,noise,dist,nx,ny = loadState()
        frames,angle,angleZ,offset = loadFrames()
    else:
        try:
            kinect = kinecter.kinect()
            blinked.switchColor('o',[1])
            kinect.start()
            kinect.backGroundSubstractor(nFrames=100)
            kinect.stop()
            blinked.switchColor('p',[1])
            while(not drawLoop):
                time.sleep(1)
            for k in range(0,6):
                time.sleep(.4)
                blinked.switchColor('r',[7])
                time.sleep(.2)
                blinked.switchColor('k',[7])

            for k in range(0,5):
                time.sleep(.3)
                blinked.switchColor('o',[7])
                time.sleep(.1)
                blinked.switchColor('k',[7])

            for k in range(0,5):
                deltaT = .3/((k+1))
                time.sleep(.9*deltaT)
                blinked.switchColor('g',[7])
                time.sleep(.1*deltaT)
                blinked.switchColor('k',[7])
            kinect.start()
            kinect.getDepthFrames(nFrames = 50,delay=.01,maxDepth=2049)
            kinect.stop()
            blinked.switchColor('c',[1])
            kinect.backgroundSubstract(blur=True,level=15)
            dX,dY,angle,angleZ = kinect.derivateFrames()
        except Exception as e: 
            print(traceback.format_exc())


        blinked.switchColor('g',[5,6])

        draw.penUp()
        #draw.squareCorner(0,0,widthPaper,heightPaper)
        blinked.switchColor('g',[5,6,7])
        nLines = 400
        size = 0


        scale,nx,ny,dist,offset =  spacer(kinect.frames)
        print("scale : "+str(scale))
        print("n     : "+str(nx))

        print("dist : "+str(dist))
        xu,yu = scaler(1,1,scale=scale,offsetX=0,offsetY=0)
        offsetA=[[-np.pi/3,0,np.pi/3],[-2*np.pi/3,np.pi,2*np.pi/3]]    
        blinked.switchColor('a',[0])
        blinked.switchColor('g',[1])




        #offsetX0 = 5-offsetY
        #offsetY0 = 5-offsetX


        nL = 30#random.randint(80,100) 


        d1 = .01 #+ (1-np.random.power(3)))   

        d2 = 1 #+ (1-np.random.power(3)))   


        speed = (.1 + .1*np.random.random())       

        crop = 0#( .0*random.random())

        noise = 0#.1*(1-np.random.power(11))

        nLStep = 1
        A0=0
        X2 = [] 

        print("----- Parameters -----")
        print("-- Lines : " + str(nL) + "--" )
        print("-- dista : " + str(d1) + "--")
        print("-- speed : " + str(speed) + "--" )
        print("-- crops : " + str(crop) + "--")
        print("-- noise : " + str(noise) + "--")
        
        frames = kinect.frames
        
        saveState(0,0,nL,scale,A0,X2,d1,d2,speed,crop,noise,dist,nx,ny)
        saveFrames(frames,angle,angleZ,offset)

    try:
        for k in range(k0,ny):
            for j2 in range(j0,nx):
                if k%2==0:
                    j=j2
                else:
                    j=nx-1-j2
                blinked.progressColor(((k*ny)+j)/(nx*ny),'v','y',[4])
                
                kFrames = random.randint(0,len(kinect.frames)-1)
                #dist = random.uniform((j-nx*math.floor(j/nx)),1+(j-nx*math.floor(j/nx)))*5
                #
                offsetY = -9999
                offsetX = -9999
                while offsetY<offset[kFrames][0] or offsetY>widthPaper+offset[kFrames][0]:
                    offsetY = offset[kFrames][0]+j*dist[0]+random.uniform(-dist[0],dist[0])

                while offsetX<offset[kFrames][1] or offsetX>heightPaper+offset[kFrames][1]:
                    offsetX = offset[kFrames][1]+k*dist[1]+0.2*random.uniform(-dist[1],dist[1])
               
                

                #print("offset : "+str((offsetX,offsetY)))
                X2 = drawing(kFrames,kinect.frames,angle,angleZ,draw,nLines = nL,scale = scale,A0=A0,\
                        offsetX = offsetX,offsetY=offsetY,figurePosition = X2,distanceLine = d1  ,distanceFigure=d2,speed = speed,cropFactor=crop,\
                        noise = noise,resolution = 0.1)
                
                while len(X2)>50000:
                    del X2[0]
                if save:
                    print("---- save -----")
                    saveState(k,j2,frames,angle,angleZ,nL,scale,A0,X2,d1,d2,speed,crop,noise,dist,nx,ny)
                    save = False
                    draw.toPosition(0,0)
                

    except Exception as e: 
        print(traceback.format_exc())
        draw.toPosition(0,0)
    draw.closeDrawer()    
    switchColor(1)

if __name__ == "__main__":
    main()


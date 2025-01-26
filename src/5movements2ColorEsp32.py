from drawer import drawerEsp as drawer
import traceback
import colorsys
from blinkt import set_pixel, set_brightness, show, clear
import numpy as np
import random
import math
from kinecter import kinecter
import time
from evdev import InputDevice, categorize, ecodes
import threading
import json
import asyncio
running = True

with open('settings.json') as f:
    settings = json.load(f)["machine"]


widthPaper = settings["size"]["x"]
heightPaper = settings["size"]["y"]
print(widthPaper+.5)
#np.random.uniform(100,400) 
#widthPaper = 148
#heightPaper = 105

from blinked import blinked

backgroundSub = False
drawLoop = False
pause = False


def mouseListener():
    global backgroundSub
    global drawLoop
    global pause
    global colorK
    pressed = []
    for k in range(0,3):
        pressed.append(False)
    dev = InputDevice('/dev/input/event0')
    while running:
        try:
            for ev in dev.read_loop():
                if ev.type == 1:
                    if ev.code == 274:
                        pressed[0] = not pressed[0]
                        if pressed[0]:
                            pause = not pause
                            print(pause)
                    elif ev.code ==273:
                        pressed[1] = not pressed[1]
                        if pressed[1]:
                            drawLoop = True
                    elif ev.code ==272:
                        pressed[2] = not pressed[2]
                        if pressed[2]:
                            backgroundSub = True
        except:
            pause = False
            time.sleep(1)
    


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
    scale = 1000
    heightMax=4000
    
    nx0=np.int(nx0)
    offsetY0 = []
    while heightMax>heightPaper-2:
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
    dist = ((widthPaper-10)-sizeImage[nx-1][0]+offset[0][0]-offset[nx-1][0])/(nx-1)
    #dist = dist - ((dist*(nx-1)+sizeImage[nx-1][0])-240)/(nx-1)
    return scale,nx,dist,offsetX,offsetY,np.array(sizeImage)


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
            noise = 0,offsetX = 0,offsetY=0,figurePosition = [],cropFactor = .3):
    global pause
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
                    and size < 100 \
                    and (dx,dy) not in linePosition\
                    and (dx1,dy1) not in imagePosition \
                    and (dx2,dy2) not in figurePosition \
                    and AZ[ky,kx]-A0<1.5 \
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
                reverse = False
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
                        and size < 100 \
                        and (dx,dy) not in linePosition\
                        and (dx1,dy1) not in imagePosition \
                        and (dx2,dy2) not in figurePosition \
                        and AZ[ky,kx]-A0<1.5 \
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



async def main():
    global pause
    mouseThread = threading.Thread(target = mouseListener)
    mouseThread.daemon = True
    mouseThread.start()
    draw = drawer.Drawer("./settings.json")
    await draw.start()
    draw.penUp()
    draw.toPosition(0,0)
    set_brightness(.05)
    blinked.switchColor('g',[0])


    while(not backgroundSub):
        time.sleep(.1)
        if pause:
            draw.toPosition(0,100)
        else:
            draw.toPosition(0,0)
    try:
        kinect = kinecter.kinect()
        blinked.switchColor('o',[1])
        kinect.start()
        kinect.backGroundSubstractor(nFrames=100)
        kinect.stop()
        blinked.switchColor('p',[1])
        while(not drawLoop):
            time.sleep(1) 
            if pause:
                draw.toPosition(0,100)
            else:
                draw.toPosition(0,0)
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
        kinect.getDepthFrames(nFrames = 100,delay=.01,maxDepth=2049)
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
    nLines = 600
    size = 0

    nx0=0
    scale,nx,dist,offsetX,offsetY,sizeImage =  spacer(kinect.frames,0,100)
    print("scale : "+str(scale))
    print("n     : "+str(nx))
    print("offsetX  : "+str(offsetX))
    print("offsetY : "+str(offsetY))
    print("dist : "+str(dist))
    print("size : "+str(sizeImage))
    nx0 = nx
    if np.max(sizeImage[nx0:nx0+nx,1])<heightPaper*.95:
        scale,nx,dist,offsetX,offsetY,sizeImage =  spacer(kinect.frames,nx0,nx*2)
        print("scale : "+str(scale))
        print("n     : "+str(nx))
        print("offsetX  : "+str(offsetX))
        print("offsetY : "+str(offsetY))
        print("dist : "+str(dist))
        print("size : "+str(sizeImage))
    xu,yu = scaler(1,1,scale=scale,offsetX=0,offsetY=0)
    offsetA=[[-np.pi/3,0,np.pi/3],[-2*np.pi/3,np.pi,2*np.pi/3]]    
    blinked.switchColor('a',[0])
    blinked.switchColor('g',[1])




    offsetX0 = 1-offsetY
    offsetY0 = 1-offsetX


    if np.random.random()<.12:
        #Nmin = np.random.randint(300,600)
        #Nmax = np.random.randint(50,200)
        Nmin = np.random.randint(50,800)
        Nmax = np.random.randint(600,1200)

        nL = np.linspace(Nmin,Nmax,nx,dtype = int)
        if random.random()<.5:
            nL = np.flip(nL) 
    else:
        #nL = random.randint(250,350) * np.ones(nx, dtype=int)  
        nL = random.randint(250,550) * np.ones(nx, dtype=int)  


    if np.random.random()<.098:
        dMin =  .05 + .5*(1-np.random.power(5))
        dMax = 1+4*np.random.random()

        d = np.linspace(dMin,dMax,nx)
        if random.random()<.5:
            d = np.flip(d) 
    else:
        d = (.2 + (1-np.random.power(3))) * np.ones(nx)  
    

    if np.random.random()<.105:
        speedMin = .1 + .2*np.random.random()
        speedMax = .5 + np.random.random()

        speed = np.linspace(speedMin,speedMax,nx)
        if np.random.random()<.5:
            speed = np.flip(speed) 
    else:
        speed = (.1 + .1*np.random.random()) * np.ones(nx)      
    
    if np.random.random()<.106:
        cropMin = 0 + .1*np.random.random()
        cropMax = .1 + .4*np.random.random()

        crop = np.linspace(cropMin,cropMax,nx)
        if random.random()<.5:
            crop = np.flip(crop) 
    else:
        crop = ( .05*random.random()) * np.ones(nx)

    if np.random.random()<.085:
        noiseMin = (1-np.random.power(11))
        noiseMax = noiseMin + 1.0*np.random.random()

        noise = np.linspace(noiseMin,noiseMax,nx)
        if np.random.random()<.5:
            noise = np.flip(noise) 
    else:
        noise = (1-np.random.power(11)) * np.ones(nx)

    colors = True
    A0=0
    X2 = []

    print("----- Parameters -----")
    print("-- Lines : " + str(nL) + "--" )
    print("-- dista : " + str(d) + "--")
    print("-- speed : " + str(speed) + "--" )
    print("-- crops : " + str(crop) + "--")
    print("-- noise : " + str(noise) + "--")
    print("-- color : " + str(colors) + "--")

    nColors = 1
    try:
        while colors:
            for j in range(0,nx):

                blinked.progressColor(j/nx,'v','y',[4])
                
                kFrames = j+nx0
                #dist = random.uniform((j-nx*math.floor(j/nx)),1+(j-nx*math.floor(j/nx)))*5
                #
                
                offsetX = offsetX0
                offsetY = offsetY0+j*dist

                #print("offset : "+str((offsetX,offsetY)))
                X2 = drawing(kFrames,kinect.frames,angle,angleZ,draw,nLines = int(nL[j]*nColors),scale = scale,A0=A0,\
                        offsetX = offsetX,offsetY=offsetY,figurePosition = X2,distanceLine = d[j]  ,speed = speed[j],cropFactor=crop[j],\
                        noise = noise[j])
            time.sleep(0)
            
            draw.toPosition(0,0)
            pause = True
            X2 = []
            A0+=math.pi/2.0
            nColors = .5+.5*np.random.random()
            
            
            

    except Exception as e: 
        print(traceback.format_exc())
        draw.toPosition(0,0)
    draw.closeDrawer()    
    switchColor(1)

if __name__ == "__main__":
    asyncio.run(main()) 

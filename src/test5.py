
from drawer import drawer
import traceback
import colorsys
from blinkt import set_pixel, set_brightness, show, clear
import numpy as np
import random
import math
from kinecter import kinecter
from blinked import blinked
import time
running = True




def switchColor(col):
    clear()
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
        kinect.backGroundSubstractor(nFrames=100)
        kinect.stop()
        blinked.switchColor('p',[1])
        time.sleep(120)
        kinect.start()
        kinect.getDepthFrames(nFrames = 30,delay=.01,maxDepth=2049)
        kinect.stop()
        blinked.switchColor('c',[1])
        kinect.backgroundSubstract(blur=True,level=20)
        dX,dY,angle,angleZ = kinect.derivateFrames()
    except Exception as e: 
        print(traceback.format_exc())
        noProblem = False


    draw = drawer.Drawer(output = False)    
    switchColor(2)
    print('---Switch is strating')
    #intializeDrawer()
    flip = False

    speed = 3
    z = kinect.frames[6]
    A = angle[6]
    Az = angleZ[6]
    idx = [6,7,8]
    nLines = 200
    size = 0
    X = []
    scale = 200
    xu,yu = scaler(1,1,scale=scale,offsetX=0,offsetY=0)
    offsetA=np.pi/3#[[-np.pi/3,0,np.pi/3],[-2*np.pi/3,np.pi,2*np.pi/3]]    
    blinked.switchColor('a',[0])
    blinked.switchColor('g',[1])
    try:
        for l in range(0,1):
            for j in range(0,1):
                nLines = 1000000#75*(3*l+j+1)

                #z = frames[j]
                #A = angle[j]
                offsetX = 5+j*80
                offsetY = 5+l*80
                for k in range(0,nLines):
                    size = 0
                    while(size == 0):
                        print('new Line : '+str(k))
                        xLines = []
                        yLines = []

                        size = 0
                        kx = random.randint(0, 639)
                        ky = random.randint(0, 479)
                        x,y = scaler(kx,ky,scale=scale,offsetX=offsetX,offsetY=offsetY)
                        x = round(x+(.5-random.random())*xu,.1)
                        y = round(y+(.5-random.random())*yu,.1)
                        zTest = z[ky,kx]
                        Atest = A[ky,kx]
                        Aztest = Az[ky,kx]
                        running = True
                        if np.isnan(zTest) or np.isnan(Atest) or np.isnan(Aztest):
                            running=False
                        if running:
                            R = random.random()*(speed * (1+np.sin(A[ky,kx]+offsetA))*np.sin(Az[ky,kx]))
                            xLines.append(round(x-R*np.cos(A[ky,kx]),.1))
                            xLines.append(round(x+R*np.cos(A[ky,kx]),.1))
                            yLines.append(round(y-R*np.sin(A[ky,kx]),.1))
                            yLines.append(round(y+R*np.sin(A[ky,kx]),.1))

                            
                            draw.lines(yLines,xLines)
                            size+=1
                
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


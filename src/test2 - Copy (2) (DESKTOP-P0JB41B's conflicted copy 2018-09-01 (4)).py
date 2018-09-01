
import drawer
import traceback
import colorsys
from blinkt import set_pixel, set_brightness, show, clear
import numpy as np
import random
import math
import kinecter
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




def scaleBack(x,y,scale=100,offsetX = 5,offsetY = 5):
    x2 = scale*x/480+offsetX
    y2 = scale*x/480+offsetX

    return x2,y2





def main():
    set_brightness(.05)
    switchColor(1)
    try:
        frames = kinecter.getFrames(30)
        dX,dY,angle,angleZ = kinecter.derivateFrames(frames)
        noProblem = True
    except:
        Exception as e: 
        print(traceback.format_exc())
        noProblem = False


    draw = drawer.Drawer(output = True)    
    switchColor(2)
    print('---Switch is strating')
    #intializeDrawer()
    flip = False

    speed = 1
    z = frames[6]
    A = angle[6]
    try:
        kx = random.randint(0, 640)
        ky = random.randint(0, 480)
        while(z[kx,ky]>0):
            dkx = kx+speed*cos(A[kx,ky])
            dky = ky+speed*cos(A[kx,ky])

        for xS in xSquare:
            draw.square(xS[0],xS[1],xS[2],xS[3]/xS[2])
            
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


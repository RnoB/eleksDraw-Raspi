
from drawer import drawer
import traceback
import colorsys
from blinkt import set_pixel, set_brightness, show, clear
import numpy as np
import random
import math
from kinecter import kinecter
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





def main():
    set_brightness(.05)
    switchColor(1)
    try:
        frames = kinecter.getFrames(30)
        dX,dY,angle,angleZ = kinecter.derivateFrames(frames)
        noProblem = True
    except Exception as e: 
        print(traceback.format_exc())
        noProblem = False


    draw = drawer.Drawer(output = False)    
    switchColor(2)
    print('---Switch is strating')
    #intializeDrawer()
    flip = False

    speed = 1
    z = frames[6]
    A = angle[6]

    nLines = 500
    size = 0
    try:
        for k in range(0,nLines):
            size = 0
            while(size == 0):
                xLines = []
                yLines = []
                X=[]
                size = 0
                kx = random.randint(0, 639)
                ky = random.randint(0, 479)
                x,y = scaler(kx,ky)
                zTest = z[ky,kx]
                Atest = A[ky,kx]
                running = True
                if np.isnan(zTest) or np.isnan(Atest):
                    running=False
                while running:
                    print('x  : '+str((x,y)))
                    print('k  : '+str((kx,ky)))
                    xLines.append(x)
                    yLines.append(y)
                    X.append((x,y))
                    dx = x+speed*np.cos(A[ky,kx])
                    dy = y+speed*np.sin(A[ky,kx])
                    print('dx : '+str((dx,dy)))
                    dxk,dyk = scaler(dx,dy,invert=True)
                    print('dk : '+str((dxk,dyk)))
                    if (dxk>-1) and (dxk<640) and (dyk>-1) and (dyk<480) and size < 100 and (dx,dy) not in X:
                        x=dx
                        y=dy
                        kx=dxk
                        ky=dyk
                        zTest = z[ky,kx]
                        Atest = A[ky,kx]
                        size +=speed
                        if np.isnan(zTest) or np.isnan(Atest):
                            running=False
                    else:
                        running = False
            draw.lines(xLines,yLines)
            
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


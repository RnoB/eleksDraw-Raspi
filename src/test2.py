
import drawer
import traceback
import colorsys
from blinkt import set_pixel, set_brightness, show, clear
import numpy as np
import random
import math
running = True




def framer(N):
    scale=(170-40.0/3.0)/N
    dx = 2.5
    dy = 5.0
    Ny = N
    Nx = int(N*1.5)
    dl = 1
    xSquare =[]
    frame = np.zeros((Nx,Ny))
    count = 1
    while (frame == 0).any():
        x = np.random.randint(0,Nx)
        y = np.random.randint(0,Ny)
        Rx = np.random.randint(-x,Nx-x)
        Ry = np.random.randint(-y,Ny-y)
        print('x : '+str(np.min((x,x+Rx)))+" y : "+str(np.min((y,y+Ry)))+' Rx : '+str(np.max((x,x+Rx)))+' Ry : '+str(np.max((y,y+Ry))))
        
        #if x+Rx<Nx and y+Ry<Ny:
            
        print(count)
        print(np.count_nonzero(frame==0))
        if (frame[np.min((x,x+Rx)):np.max((x,x+Rx))+1,np.min((y,y+Ry)):np.max((y,y+Ry))+1]==0).all():
            frame[np.min((x,x+Rx)):np.max((x,x+Rx))+1,np.min((y,y+Ry)):np.max((y,y+Ry))+1] = count
            count += 1
        if np.count_nonzero(frame==0)==1:
            frame[frame==0]=count
            count += 1
    print(frame)
    for k in range(1,count):
        X = np.where(frame == k)

        xSquare.append((dx+scale*(X[0][-1]+X[0][0]+1)/2,dy+scale*(X[1][-1]+X[1][0]+1)/2,-dl+scale*(X[0][-1]-X[0][0]+1)/2,-dl+scale*(X[1][-1]-X[1][0]+1)/2))
    print(xSquare)
    return xSquare

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










def main():
    set_brightness(.05)
    switchColor(1)
    draw = drawer.Drawer(output = True)    
    switchColor(2)
    print('---Switch is strating')
    #intializeDrawer()
    flip = False

    xSquare = framer(6)

    try:
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


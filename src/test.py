
import drawer
import traceback
import colorsys
from blinkt import set_pixel, set_brightness, show, clear
import numpy as np
import random
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






def main():
    set_brightness(.05)
    switchColor(1)
    draw = drawer.Drawer(output = True)    
    switchColor(2)
    print('---Switch is strating')
    #intializeDrawer()
    flip = False

    xSquare = []
    for k in range(0,4):
        checked = False
        while not checked:
            x0 = 50 + 160*random.random()
            y0 = 50 + 160*random.random()
            R0 = 40*random.random()
            if x0-R0>10 and x0+R0<250  and y0-R0>10 and y0+R0<170:
                checked  = True  
        xSquare.append([x0,y0,R0])
    print('and the sqaures are : ')
    print(xSquare)

    try:
        for xS in xSquare:
            draw.square(xS[0],xS[1],xS[2]*2)
            for k in np.arange(10,145,40):
                x = np.arange(10,250,.2)
                if flip:
                    x = np.flip(x)
                y = 10+k*1.2+2*np.sin(2*math.pi*((x-10)/240)**(1+k/200))
                y2 = np.copy(y[(x>xS[0]-xS[2]) & (x<xS[0]+xS[2]) & (y>xS[0]-xS[2]) & (y<yS[0]+xS[2]) ])
                x2 = np.copy(x[(x>xS[0]-xS[2]) & (x<xS[0]+xS[2]) & (y>xS[0]-xS[2]) & (y<yS[0]+xS[2]) ])
                draw.lines(x2,y2)
                flip = not flip
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
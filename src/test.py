
import drawer
import traceback
import colorsys
from blinkt import set_pixel, set_brightness, show, clear
import numpy as np

running = True





def switchColor(col):
    clear()
    if col == 0:
        for k in range(0,7):
            set_pixel(k,0,255,0)
    if col == 1:
        for k in range(0,7):
            set_pixel(k,255,0,0)
    if col == 2:
        for k in range(0,7):
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
    set_brightness(.2)
    switchColor(1)
    draw = drawer.Drawer()    
    switchColor(2)
    print('---Switch is strating')
    #intializeDrawer()
    try:
        for k in range(0,120):
            x = np.arange(20,220,.2)
            draw.lines(x,20+k*1.2+2*np.sin(((x-20)/3)**(1+k/200)))
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
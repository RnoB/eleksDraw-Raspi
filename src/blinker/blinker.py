
from blinkt import set_pixel, set_brightness, show, clear
import colorsys
import numpy as np



def clear():
    clear()


def switchColor(col,pix = np.arange(0,8,1),brightness = .1,clear = False):
    #clear()
    if clear:
        clear()
    set_brightness(brightness)
    if isinstance(col,str):
        r=0
        g=0
        b=0
        if col == 'r':
            r=1
        elif col == 'g':
            g=1
        elif col == 'b':
            b=1
        elif col =='y':
            r=1
            g=1
        elif col == 'c':
            g=1
            b=1
        elif col == 'm':
            r=1
            b=1
        elif col == 'o':
            r=1
            g=.5
        elif col == 'p':
            r=1
            b=.5
        elif col == 'a':
            r=.5
            g=1
        elif col = 'v':
            r=.5
            b=.5
        elif col = 'f':
            g=1
            b=.5
        elif col = 'd':
            g=.5
            b=1
    else:
        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(col, 1.0, 1.0)]
    for k in pix:
        set_pixel(k,r,g,b)
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

from blinkt import set_pixel, set_brightness, show, clear
import colorsys
import numpy as np



def clear():
    clear()


def defColor(col):
    if isinstance(col,str):
        r=0
        g=0
        b=0
        if col == 'r':
            r=255
        elif col == 'g':
            g=255
        elif col == 'b':
            b=255
        elif col =='y':
            r=255
            g=255
        elif col == 'c':
            g=255
            b=255
        elif col == 'm':
            r=255
            b=255
        elif col == 'o':
            r=255
            g=127
        elif col == 'p':
            r=255
            b=127
        elif col == 'a':
            r=127
            g=255
        elif col = 'v':
            r=127
            b=127
        elif col = 'f':
            g=255
            b=127
        elif col = 'd':
            g=127
            b=255
    else:
        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(col, 1.0, 1.0)]
    return r,g,b

def switchColor(col,pix = np.arange(0,8,1),brightness = .1,clear = False):
    #clear()
    if clear:
        clear()
    set_brightness(brightness)
    r,g,b = defColor(col)
    for k in pix:
        set_pixel(k,r,g,b)
    show()

def progressColor(progress,col1,col2,pix = [0]):
    r1,g1,b1 = defColor(col1)
    r2,g2,b2 = defColor(col2)

    dr = r2-r1
    dg = g2-g1
    db = b2-b1

    r = r1+progress*dr
    g = g1+progress*dg
    b = b1+progress*db
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
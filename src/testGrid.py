import numpy as np

from drawer import drawer


def main():



    draw = drawer.Drawer(dx=450,dy=230)    
    draw.penInvert()
    draw.penUp()
    draw.toPosition(0,0)




if __name__ == "__main__":
    main()

    X = np.arange(0,60,1)
    Y = np.arange(-20,20,1)

    for k in range(1,len(Y)):
        for j in range(1,len(X)):
            xLines = [X[j-1],X[j]]
            xLines = [Y[k],Y[k]]
            draw.lines(yLines,xLines)

    for k in range(1,len(X)):
        for j in range(1,len(Y)):
            xLines = [X[k],X[k]]
            xLines = [Y[j-1],Y[j]]
            draw.lines(yLines,xLines)
    draw.toPosition(0,0)
    draw.closeDrawer()

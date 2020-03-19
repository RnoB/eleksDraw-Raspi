import numpy as np

from drawer import drawer


def main():



    draw = drawer.Drawer(dx=450,dy=230)    
    draw.penInvert()
    draw.penUp()
    draw.toPosition(0,0)
    
    X = np.arange(0,600,10)
    Y = np.arange(-200,200,10)

    for k in range(1,len(X)):
        for j in range(1,len(Y)):
            xLines = [X[k],X[k]]
            yLines = [Y[j-1],Y[j]]
            draw.lines(xLines,yLines)

    for k in range(1,len(Y)):
        for j in range(1,len(X)):
            xLines = [X[j-1],X[j]]
            yLines = [Y[k],Y[k]]
            draw.lines(xLines,yLines)

  
    draw.toPosition(0,0)
    draw.closeDrawer()




if __name__ == "__main__":
    main()



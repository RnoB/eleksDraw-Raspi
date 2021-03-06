import numpy as np

from drawer import drawer


def main():



    draw = drawer.Drawer(dx=350,dy=230)    
    draw.penInvert()
    draw.penUp()
    draw.toPosition(0,0,speed=500)
    
    X = np.arange(0,600,60)
    Y = np.arange(-200,200,60)
    print(X)
    print(Y)
    for k in range(0,len(X)):
        for j in range(1,len(Y)):
            xLines = [X[k],X[k]]
            yLines = [Y[j-1],Y[j]]
            draw.lines(yLines,xLines,polar = True,speed=300)

    for k in range(0,len(Y)):
        for j in range(1,len(X)):
            xLines = [X[j-1],X[j]]
            yLines = [Y[k],Y[k]]
            draw.lines(yLines,xLines,polar = True,speed=300)

  
    draw.toPosition(0,0)
    draw.closeDrawer()




if __name__ == "__main__":
    main()



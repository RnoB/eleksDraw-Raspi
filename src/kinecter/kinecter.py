#import the necessary modules
import freenect
import cv2
import numpy as np
import time

import random



kinectWidth = 640
kinectHeight = 480


def kinectFrame(width,height):
    kinectWidth = width
    kinectHeight = height


def get_depth():
    print('get depth')
    array = freenect.sync_get_depth()[0]
    print('got depth')
    array=np.float32(array)
    return array


def getFrames(nFrames=30,delay=.5,maxDepth = 945):
    frames = []
    
    for k in range(0,nFrames):
        depth = get_depth()
        depth[depth>maxDepth]=np.nan
        if np.isnan(depth).all() or len(depth[~np.isnan(depth)])<20000:
            print('all nan')
        else:
        
        
            depthMin = np.min(depth[~np.isnan(depth)])
            depthMax = np.max(depth[~np.isnan(depth)])
        
            frames.append(1-(depth-depthMin)/(depthMax-depthMin))
        time.sleep(delay)
    return frames


def derivateFrames(frames):
    dX = []
    dY = []
    angle = []
    angleZ = []
    for frame in frames:
        dX.append(cv2.Sobel(frame,cv2.CV_64F,1,0,ksize=-1))
        dY.append(cv2.Sobel(frame,cv2.CV_64F,0,1,ksize=-1))
        angle.append(np.arctan2(dX[-1],dY[-1]))
        dZ = (dX[-1]+dY[-1])/2
        norm = np.sqrt(dX[-1]**2+dY[-1]**2)
        angleZ.append(np.arctan2(norm,dZ))
    return dX,dY,angle,angleZ




def scaler(x,y,scale=100,offsetX = 5,offsetY = 5,invert=False):
    if invert:
        x2 = np.int(kinectHeight*(x-offsetX)/scale)
        y2 = np.int(kinectHeight*(y-offsetY)/scale)
    else:
        x2 = scale*x/kinectHeight+offsetX
        y2 = scale*y/kinectHeight+offsetY

    return x2,y2


def round(x, base=1):
    return base * np.round(x/base)


def drawGradient(z,A,nLines = 200,speed =1,scale=100,offsetX=5,offsetY=5,offsetA = 0,sizeMax = 100,xMin=5,xMax=260,yMin=5,yMax=170):
    X = []
    xLines= []
    yLines= []
    xu,yu = scaler(1,1,scale=scale,offsetX=0,offsetY=0)
    for k in range(0,nLines):
        print(k)
        size = 0
        while(size == 0):
            print('new Line : '+str(k))
            xLines = []
            yLines = []

            size = 0
            kx = random.randint(0, kinectWidth-1)
            ky = random.randint(0, kinectHeight-1)
            x,y = scaler(kx,ky,scale=scale,offsetX=offsetX,offsetY=offsetY)
            x = round(x+(.5-random.random()),.1)
            y = round(y+(.5-random.random()),.1)
            zTest = z[ky,kx]
            Atest = A[ky,kx]
            running = True
            if np.isnan(zTest) or np.isnan(Atest):
                running=False
            while running:
                xLines.append(x)
                yLines.append(y)
                X.append((x,y))
                dx = round(x+speed*np.cos(offsetA+A[ky,kx]),.1)
                dy = round(y+speed*np.sin(offsetA+A[ky,kx]),.1)
                
                dxk,dyk = scaler(dx,dy,scale=scale,offsetX=offsetX,offsetY=offsetY,invert=True)
                
                if (dxk>-1) and (dxk<640) and (dyk>-1) and (dyk<480) and size < sizeMax and dx>xMin and dx<xMax and dy>yMin and dy<yMax and (dx,dy) not in X:
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
    return xLines,yLines


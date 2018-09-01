#import the necessary modules
import freenect
import cv2
import numpy as np
import time



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

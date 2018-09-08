#import the necessary modules
import freenect
import cv2
import numpy as np
import time
from blinkt import set_pixel, set_brightness, show, clear
import random



def round(x, base=1):
    return base * np.round(x/base)


def switchColor(col):
    #clear()
    if col == 0:
        for k in range(2,3):
            set_pixel(k,0,255,0)
    if col == 1:
        for k in range(2,3):
            set_pixel(k,255,0,0)
    if col == 2:
        for k in range(2,3):
            set_pixel(k,0,0,255)
    show()


class kinect:    



    def kinectFrame(self,width,height):
        kinectWidth = width
        kinectHeight = height







    def get_depth(self):
        print('get depth')
        array = freenect.sync_get_depth()[0]
        print('got depth')
        array=np.float32(array)
        return array


    def getFrames(self,nFrames=30,delay=.5,maxDepth = 945):
        frames = []
        
        for k in range(0,nFrames):
            switchColor(0)
            depth = get_depth()
            switchColor(1)
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




    def scaler(self,x,y,scale=100,offsetX = 5,offsetY = 5,invert=False):
        if invert:
            x2 = np.int(kinectHeight*(x-offsetX)/scale)
            y2 = np.int(kinectHeight*(y-offsetY)/scale)
        else:
            x2 = scale*x/kinectHeight+offsetX
            y2 = scale*y/kinectHeight+offsetY

        return x2,y2


    def depthAcq(self,dev, data, timestamp):

        switchColor(0)
        self.frames.append(data)
        switchColor(1)


    def getDepthFrames(self,delay=.01,nFrames=10):
        self.nFrames = nFrames
        self.delay = delay
        freenect.start_depth(self.dev)
        freenect.set_depth_callback(self.dev,self.depthAcq)
        self.frames = []
        
        while len(self.frames)<nFrames:
            
            freenect.process_events(self.ctx)
            time.sleep(delay)

    def start(self,degs=10):
        self.ctx = freenect.init()
        if not self.ctx:
            freenect.error_open_device()
        self.dev = freenect.open_device(self.ctx, 0)
        if not self.dev:
            freenect.error_open_device()
        freenect.set_tilt_degs(self.dev,-degs)
        freenect.set_tilt_degs(self.dev,degs)
        self.intialised == True
        print('kinect Started')

    def stop(self):
        freenect.close_device(self.dev)
        freenect.shutdown(self.ctx)
        print('kinect Stopped')

    def __init__(self,output = False,nFrames = 10,delay = .5):
        self.kinectWidth = 640
        self.kinectHeight = 480
        self.intialised = False
        self.record = False

        self.ctx = []
        self.dev = []
        self.frames = []
        self.nFrames = nFrames
        self.delay = delay






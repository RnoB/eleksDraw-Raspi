import asyncio
import telnetlib3
import numpy as np
import json


class Drawer:

    def sendCommand(self,cmd):
        self.writer.write(cmd+'\r\n')

    def penUp(self):
        gCode = 'G1Z'+str(self.pen["up"])+'F'+str(self.pen["speed"])
        self.sendCommand(gCode)

    def penDown(self):
        gCode = 'G1Z'+str(self.pen["down"])+'F'+str(self.pen["speed"])
        self.sendCommand(gCode)

    def toPosition(self,x,y):
        x0 = self.invert[0] * x
        y0 = self.invert[1] * y
        gCode = 'G1X'+str(x0)+'Y'+str(y0)+'F'+str(self.speed)
        self.sendCommand(gCode)

    def lines(self,X):
        X = np.array(X)
        self.toPosition(X[0,0],X[0,1])
        self.penDown()
        for k in range(1,np.shape(np.array(X))[0]):
            self.toPosition(X[k,0],X[k,1])
        self.penUp()


    async def start(self):
        self.reader, self.writer = await telnetlib3.open_connection(self.settings["ip"], self.settings["port"])
        self.sendCommand("G90")
        self.sendCommand("G10")
        self.sendCommand("G21")
        
        


    def __init__(self,path = "settings.json"):
        with open('settings.json') as f:
            self.settings = json.load(f)["machine"]
        self.size = self.settings["size"]
        self.invert = [int(1-2*self.settings["invert"]["x"]),int(1-2*self.settings["invert"]["y"])]
        self.speed = self.settings["speed"]
        self.pen = self.settings["pen"]
        self.offset = self.settings["offset"] 

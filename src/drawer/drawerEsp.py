import asyncio
import telnetlib3
import numpy as np
import json


class Drawer:

    def closeDrawer(self):
        self.toPosition(0,0)

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

    def lines(self,x,y,xOffset=0,yOffset=0,speed=2000,polar=False,smooth=False):
        self.toPosition(x[0]+xOffset,y[0]+yOffset)
        self.penDown()
        k0=0
        try:
            for k in range(0,len(x)):
                k0 = k
                
                self.toPosition(x[k]+xOffset,y[k]+yOffset)
        except:
            print('--- CRASH !!!! ---')
            print("length : "+str(len(x)))
            print("  k0   : "+str(k0))
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

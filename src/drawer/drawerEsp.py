import asyncio
import telnetlib3
import numpy as np
import json
import time

class Drawer:

    async def closeDrawer(self):
        await self.toPosition(0,0)

    async def sendCommand(self,cmd):
        self.writer.write(cmd+'\r\n')
        reply = await self.reader.read()
        reply print('reply:', reply)

    async def penUp(self):
        gCode = 'G1Z'+str(self.pen["up"])+'F'+str(self.pen["speed"])
        await self.sendCommand(gCode)

    async def penDown(self):
        gCode = 'G1Z'+str(self.pen["down"])+'F'+str(self.pen["speed"])
        await self.sendCommand(gCode)

    async def toPosition(self,x,y):
        x1 = self.invert[0] * x
        y1 = self.invert[1] * y
        gCode = 'G1X'+str(x1)+'Y'+str(y1)+'F'+str(self.speed)
        await self.sendCommand(gCode)
        time.sleep(np.sqrt((x1-self.x0)**2+(y1-self.y0)**2)*60/self.speed)
        self.x0 = x1
        self.y0 = y1

    async def lines(self,x,y,xOffset=0,yOffset=0,speed=2000,polar=False,smooth=False):
        await self.toPosition(x[0]+xOffset,y[0]+yOffset)
        await self.penDown()
        k0=0
        try:
            for k in range(0,len(x)):
                k0 = k
                
                await self.toPosition(x[k]+xOffset,y[k]+yOffset)
        except:
            print('--- CRASH !!!! ---')
            print("length : "+str(len(x)))
            print("  k0   : "+str(k0))
        await self.penUp()


    async def start(self):
        self.x0 = 0
        self.y0 = 0
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

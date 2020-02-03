import asyncio
from evdev import InputDevice, categorize, ecodes

dev = InputDevice('/dev/input/event0')
async def helper(dev):
     async for ev in dev.async_read_loop():
        if ev.type == 1:
            print("--- Click ---")
            if ev.value == 0:
                print("Released")
            elif ev.value == 1:
                print("Pressed")
            if ev.code == 272:
                print("Left")
            elif ev.code ==274:
                print("Middle")
            elif ev.code ==273:
                print("Right")
        if ev.type == 2:
            print("-- Movement --")
            if ev.code == 0:
                print("X : "+str(ev.value))
            if ev.code == 1:
                print("Y : "+str(ev.value))
            if ev.code == 6:
                print("WheelX : "+str(ev.value))
            if ev.code == 8:
                print("WheelY : "+str(ev.value))
loop = asyncio.get_event_loop()
loop.run_until_complete(helper(dev))

import drawer
import time
import math
import numpy as np
import random
import sys
import os
import traceback
import threading
import socket
import drawIP
s = []
x = 0
y = 0


def giveStatus(ip):
    backlog = 1  # how many connections to accept
    maxsize = 28
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    binded = False
    while not binded:
        try:
            server.bind((ip,statusPort))
            binded = True
        except:
            print('- Give Status -- binding failed')
            binded = False
            time.sleep(20)
    server.listen(1)
    while running:
        print('--- waiting for a connection')
        try:
            connection, client_address = server.accept()
            print('------ Connection coming from ' + str(client_address))



            code = struct.unpack('i',connection.recv(4))[0]
            print('------ code : '+ str(code))
            if code == requestStatusCode:
                data = struct.pack('i', sendStatusCode)
                try:
                    connection.sendall(data)
                except:
                    print('sending did not work :/ but better not break everything')
        except:
            pass


def receiveDirection(IP,PORT):

    backlog = 1  # how many connections to accept
    maxsize = 28
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    binded = False
    print('---- Stimuli Updater')
    while not binded:
        try:
            server.bind((IP,PORT))
            binded = True
        except:
            print(IP)
            print('- Wait for Stimuli Update -- binding failed')
            binded = False
    server.listen(1)
    print('---- Stimuli Updater is binded on : '+ IP +' with port : '+ str(PORT))
    while running:
        print('--- waiting for a connection')
        try:
            connection, client_address = server.accept()
            print('------ Connection coming from ' + str(client_address))



            mess = struct.unpack('ddi',connection.recv(20))[0]
            code = mess[2]
            x = mess[0]
            y = mess[1]
            print('------ code : '+ str(code[0]))
            if code == drawIP.drawerCode['penUp']:
                drawer.penUp()
            if code == drawIP.drawerCode['penDown']:
                drawer.penDown()
            if code == drawIP.drawerCode['toPosition']:
                drawer.toPosition(x,y)

        except:
            pass

def main():
    
    receiveThread = threading.Thread(target=receiveDirection, args=(drawIP.drawerIP, drawIP.drawerPort))
    receiveThread.daemon = True
    receiveThread.start()


    statusThread = threading.Thread(target = giveStatus, args=(drawIP.drawerIP,))
    statusThread.daemon = True
    statusThread.start()

    t0 = time.time()

    while running:
        t = time.time()-t0
        time.sleep(3600)
        print(">>>>>>>>>>>> the drawer is in service since " + str(int(t/3600)) +" hours")






if __name__ == '__main__':
    main()

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
import struct
s = []
x = 0
y = 0
running = True
draw = []



def sendCommand(code,x = 0,y = 0):
    dataRec =[]
    socketClient = socket.socket()
    socketClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connect = 0
    



    while connect == 0:
        try:
            socketClient.connect((drawIP.drawerIP, drawIP.drawerPort))
            connect = 1
        except:
            connect = 0
    data = struct.pack('ddi',x,y,code)
    socketClient.sendall(data)

    socketClient.shutdown(socket.SHUT_RDWR)
    socketClient.close()
    return dataRec


def sendLines(x,y):
    dataRec =[]
    socketClient = socket.socket()
    socketClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connect = 0
    



    while connect == 0:
        try:
            socketClient.connect((drawIP.drawerIP, drawIP.drawerPort))
            connect = 1
        except:
            connect = 0
    data = struct.pack('ddi',x[0],y[0],drawIP.drawerCode['lineBegin'])
    socketClient.sendall(data)
    print('here')
    for k in range(1,len(x)):
        data = struct.pack('ddi',x[k],y[k],drawIP.drawerCode['toPosition'])
        socketClient.sendall(data)
    data = struct.pack('ddi',x[0],y[0],drawIP.drawerCode['lineEnd'])
    socketClient.sendall(data)
    print('here')

    socketClient.shutdown(socket.SHUT_RDWR)
    socketClient.close()
    return dataRec

def pen(position):
    dataRec =[]
    socketClient = socket.socket()
    socketClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connect = 0
    
    while connect == 0:
        try:
            socketClient.connect((drawIP.drawerIP, drawIP.drawerPort))
            connect = 1
        except:
            connect = 0
    if position == "down":
        code = drawIP.drawerCode['penDown']
    else:
        code = drawIP.drawerCode['penUp']

    data = struct.pack('ddi',x[0],y[0],code)
    socketClient.sendall(data)
    
    socketClient.shutdown(socket.SHUT_RDWR)
    socketClient.close()
    return dataRec

def sendPosition(x,y):
    dataRec =[]
    socketClient = socket.socket()
    socketClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connect = 0
    



    while connect == 0:
        try:
            socketClient.connect((drawIP.drawerIP, drawIP.drawerPort))
            connect = 1
        except:
            connect = 0
    
    data = struct.pack('ddi',x[k],y[k],drawIP.drawerCode['toPosition'])
    socketClient.sendall(data)

    socketClient.shutdown(socket.SHUT_RDWR)
    socketClient.close()
    return dataRec

def giveStatus(ip):
    global running
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
    global running
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
        #try:
            connection, client_address = server.accept()
            print('------ Connection coming from ' + str(client_address))



            message = struct.unpack('ddi',connection.recv(20))
            code = message[2]
            x = message[0]
            y = message[1]
            print('------ code : '+ str(code))
            if code == drawIP.drawerCode['penUp']:
                draw.penUp()
            if code == drawIP.drawerCode['penDown']:
                draw.penDown()
            if code == drawIP.drawerCode['toPosition']:
                draw.toPosition(x,y)
            if code == drawIP.drawerCode['lineBegin']:
                draw.toPosition(x,y)
                draw.penDown()
                line = True
                while line:
                    message = struct.unpack('ddi',connection.recv(20))
                    code = message[2]
                    if code == drawIP.drawerCode['lineEnd']:
                        draw.penUp()
                        line = False
                    else:
                        x = message[0]
                        y = message[1]
                        draw.toPosition(x,y)


        #except:
        #    pass

def main():
    global running
    global draw
    draw = drawer.Drawer()
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

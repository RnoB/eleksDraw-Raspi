import numpy
import threading
import time
import socket
import struct
import numpy as np

drawerIP = "192.168.0.100"
drawerPort = 9997

drawerCode = {'penUp' : 21,'penDown' : 21,
              'toPosition' : 22,
              'line' : 31,'lineEnd' : 32}


def drawerSend(code,x,y):
    dataRec =[]
    socketClient = socket.socket()
    socketClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connect = 0
    



    while connect == 0:
        try:
            socketClient.connect((drawerIP, drawerPort))
            connect = 1
        except:
            connect = 0
    data = struct.pack('ddi',x,y,code)
    socketClient.sendall(data)

    socketClient.shutdown(socket.SHUT_RDWR)
    socketClient.close()
    return dataRec


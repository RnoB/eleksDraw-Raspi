import numpy
import threading
import time
import socket
import struct
import numpy as np

drawerIP = "192.168.0.100"
drawerIP2 = "192.168.0.101"
drawerPort = 9997

drawerCode = {'penUp' : 21,'penDown' : 22,
              'toPosition' : 31,
              'lineBegin' : 41,'lineEnd' : 42}



 
import pprint
import sys
import time

import socket
import pickle

import cv2
import numpy as np
import zmq


def producer(path):
    context = zmq.Context()
    zmq_sockets = []
    port = int(sys.argv[3])
    for i in range(int(sys.argv[2])):
        # to send ports data  
        zmq_sockets.append(context.socket(zmq.PUSH))
        zmq_sockets[i].bind("tcp://127.0.0.1:%s" % (port + i))
        
    vidcap = cv2.VideoCapture(path)
    success, image = vidcap.read()
    count = 0

    while success:
        success, image = vidcap.read()
        if (success == True):
            msg={'image':image,'frame_num':count}
            (zmq_sockets[count % (int(sys.argv[2]))]).send(pickle.dumps(msg))
        count += 1
        #print(count, image)


path = sys.argv[1]

producer(path)

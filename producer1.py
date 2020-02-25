import pprint
import sys
import time

import cv2
import numpy as np
import zmq


def send_array(socket, A, f_num, flags=0, copy=True, track=False):
    """send a numpy array with metadata"""
    md = dict(
        dtype='uint8',
        shape=A.shape,
        frame_num=f_num,
    )
    socket.send_json(md, flags | zmq.SNDMORE)
    return socket.send(A, flags, copy=copy, track=track)


def producer(path):
    context = zmq.Context()
    # Start your result manager and workers before you start your producers
    # print(type(int(sys.argv[2])))
    zmq_sockets = []
    port = int(sys.argv[3])
    for i in range(int(sys.argv[2])):
        # to send ports data  
        zmq_sockets.append(context.socket(zmq.PUSH))
        zmq_sockets[i].bind("tcp://127.0.0.1:%s" % (port + i))
        # print('tcp://127.0.0.1:%s'%(port+i))

    vidcap = cv2.VideoCapture(path)
    success, image = vidcap.read()
    count = 0

    while success:
        success, image = vidcap.read()
        if (success == True):
            send_array(zmq_sockets[count % (int(sys.argv[2]))], image, count)
        count += 1
        # print(count, image)


path = sys.argv[1]
# print(path)
producer(path)

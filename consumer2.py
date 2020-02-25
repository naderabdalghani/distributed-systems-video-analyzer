import pprint
import random
import sys
import time

import cv2
import imutils
import numpy
import zmq
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu


def recv_array(socket, flags=0, copy=True, track=False):
    """recv a numpy array"""
    md = socket.recv_json(flags=flags)
    msg = socket.recv(flags=flags, copy=copy, track=track)
    buf = memoryview(msg)
    A = numpy.frombuffer(buf, dtype=md['dtype'])
    return A.reshape(md['shape']), md['frame_num']


def send_array(socket, A, f_num, flags=0, copy=True, track=False):
    """send a numpy array with metadata"""
    md = dict(
        dtype='uint8',
        shape=A.shape,
        frame_num=f_num,
    )
    socket.send_json(md, flags | zmq.SNDMORE)
    return socket.send(A, flags, copy=copy, track=track)


def consumer():
    context = zmq.Context()
    PULL_port = int(sys.argv[1])
    PUSH_port = int(sys.argv[2])

    print("I am consumer #%s" % (PULL_port))

    # recieve work
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.bind("tcp://127.0.0.1:%s" % PULL_port)

    # send work
    consumer_sender = context.socket(zmq.PUSH)
    consumer_sender.connect("tcp://127.0.0.1:%s" % PUSH_port)

    while True:
        print("inside while loop")
        image, f_num = recv_array(consumer_receiver)
        #consumer 2 received image.
        print(f_num, image)
        #cnts,_ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #cnts = imutils.grab_contours(cnts)
        send_array(consumer_sender, image, f_num)
        
        # time.sleep(1)


consumer()

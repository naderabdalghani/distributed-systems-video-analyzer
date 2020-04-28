import pprint
import random
import sys
import time

import socket
import pickle


import cv2
import numpy
import zmq
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu


def consumer():
    context = zmq.Context()
    PULL_port = int(sys.argv[1])
    PUSH_port = int(sys.argv[2])

    print("I am consumer #%s" % (PULL_port))

    # recieve work
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.connect("tcp://127.0.0.1:%s" % PULL_port)

    # send work
    consumer_sender = context.socket(zmq.PUSH)
    consumer_sender.connect("tcp://127.0.0.1:%s" % PUSH_port)

    while True:
        recv_msg = pickle.loads(consumer_receiver.recv())
        image = recv_msg['image']
        f_num = recv_msg['frame_num']

        image = rgb2gray(image)
        thresh = threshold_otsu(image)  # Calculate The Best Threshold
        image = image > thresh  # Apply Threshold
        msg={'image':image,'frame_num':f_num}
        consumer_sender.send(pickle.dumps(msg))
        print(f_num, image)


consumer()

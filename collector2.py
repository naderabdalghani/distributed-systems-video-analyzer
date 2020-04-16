import pprint
import sys
import time

import socket
import pickle


import cv2
import numpy
import zmq


def recv_array(socket, flags=0, copy=True, track=False):
    md = socket.recv_json(flags=flags)
    msg = socket.recv(flags=flags, copy=copy, track=track)
    #buf = memoryview(msg)
    A = numpy.frombuffer(msg, dtype=md['dtype'])
    return A.reshape(md['shape']), md['frame_num']


def result_collector():
    context = zmq.Context()
    results_receiver1 = context.socket(zmq.PULL)
    print("I am the final collector waiting at port #%s" % (int(sys.argv[1])))
    results_receiver1.bind("tcp://127.0.0.1:%s" % (int(sys.argv[1])))
    file1 = open("output.txt", "a")
    while True:
        recv_msg = pickle.loads(results_receiver1.recv())
        cnts = recv_msg['image']
        f_num = recv_msg['frame_num']
        print(cnts,f_num)
        file1.write("Frame # {} : {}\n\n".format(f_num,cnts))
        #file1.close()
 


result_collector()

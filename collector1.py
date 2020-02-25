import pprint
import sys
import time

import cv2
import numpy
import zmq


def send_array(socket, A, f_num, flags=0, copy=True, track=False):
    """send a numpy array with metadata"""
    md = dict(
        dtype='uint8',
        shape=A.shape,
        frame_num=f_num,
    )
    socket.send_json(md, flags | zmq.SNDMORE)
    print("sending from collector 1")
    return socket.send(A, flags, copy=copy, track=track)


def recv_array(socket, flags=0, copy=True, track=False):
    """recv a numpy array"""
    md = socket.recv_json(flags=flags)
    msg = socket.recv(flags=flags, copy=copy, track=track)
    buf = memoryview(msg)
    A = numpy.frombuffer(buf, dtype=md['dtype'])
    return A.reshape(md['shape']), md['frame_num']


def result_collector():
    print()
    PUSH_PORT = int(sys.argv[1])+2000
    print("I am collector #%s" % (PUSH_PORT))
    receiverSwitcher = True

    context = zmq.Context()
    results_receiver1 = context.socket(zmq.PULL)
    results_receiver1.bind("tcp://127.0.0.1:%s" % (int(sys.argv[1])))

    results_sender1 = context.socket(zmq.PUSH)
    results_sender2 = context.socket(zmq.PUSH)
    results_sender1.connect("tcp://127.0.0.1:%s" % PUSH_PORT)
    results_sender2.connect("tcp://127.0.0.1:%s" % PUSH_PORT)

    # results_receiver2 = context.socket(zmq.PULL)
    # print(int(sys.argv[1]))
    while True:
        image, f_num = recv_array(results_receiver1)
        # print("printing from collector 1")
        print(f_num, image)
        if(receiverSwitcher):
            send_array(results_sender1, image, f_num)
            print("sender1\n")
            receiverSwitcher = False
        else:
            send_array(results_sender2, image, f_num)
            print("sender2\n")
            receiverSwitcher = True
        


result_collector()

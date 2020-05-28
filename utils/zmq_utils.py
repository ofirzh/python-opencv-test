# https://pyzmq.readthedocs.io/en/latest/serialization.html#using-your-own-serialization
import zmq
import numpy


class ZMQInput:
    def __init__(self, name, max_size=200):
        self.context = zmq.Context()
        self.receiver = self.context.socket(zmq.PULL)
        self.receiver.setsockopt(zmq.RCVHWM, max_size)
        self.receiver.connect(f"ipc:///tmp/{name}")

    def receive(self):
        return recv_array(self.receiver)


class ZMQOutput:
    def __init__(self, name, max_size=200):
        self.context = zmq.Context()
        self.sender = self.context.socket(zmq.PUSH)
        self.sender.setsockopt(zmq.SNDHWM, max_size)
        self.sender.bind(f"ipc:///tmp/{name}")

    def send(self, array):
        return send_array(self.sender, array)


def send_array(socket, A, flags=0, copy=False, track=False):
    """send a numpy array with metadata"""
    md = dict(
        dtype=str(A.dtype),
        shape=A.shape,
    )
    socket.send_json(md, flags|zmq.SNDMORE)
    return socket.send(A, flags, copy=copy, track=track)


def recv_array(socket, flags=0, copy=False, track=False):
    """recv a numpy array"""
    md = socket.recv_json(flags=flags)
    msg = socket.recv(flags=flags, copy=copy, track=track)
    buf = memoryview(msg)
    A = numpy.frombuffer(buf, dtype=md['dtype'])
    return A.reshape(md['shape'])
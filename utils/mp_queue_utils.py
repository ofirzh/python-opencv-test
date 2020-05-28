from time import sleep
from multiprocessing import Queue


class SizedQueue:
    def __init__(self, max_size):
        self.maxsize = max_size
        self.q = Queue()

    def send(self, msg):
        while self.q.qsize() > self.maxsize:
            sleep(0.3)
        self.q.put(msg)

    def receive(self):
        return self.q.get()

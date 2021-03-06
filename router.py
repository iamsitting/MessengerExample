import zmq
import threading
from constants import *


class Router(threading.Thread):
    def __init__(self, threadID, name, context):
        threading.Thread.__init__(self)
        self.stoprequest = threading.Event()
        self.threadID = threadID
        self.name = name
        self.context = context
        self.sock = self.context.socket(zmq.ROUTER)
        self.sock.identity = 'router'
        self.sock.setsockopt(zmq.LINGER, 0)
        self.sock.bind(IPC_ADDR)
        self.message = None
        self.poller = zmq.Poller()
        self.poller.register(self.sock, zmq.POLLIN)

    def run(self):
        while not self.stoprequest.is_set():
            socks = dict(self.poller.poll(1000))
            if self.sock in socks and socks[self.sock] == zmq.POLLIN:
                sender, self.message = self.sock.recv_multipart()
            if self.message is not None:
                if sender == 'GUI' or sender == 'CLI':
                    if self.message == 'WINDOWCLOSED':
                        # print '{0}:{1}'.format('q2', self.message)
                        self.sock.send_multipart(['web-dealer', self.message])
                        self.sock.close()
                        return -1
                    else:
                        tprint('{0}:{1}'.format(sender, self.message))
                        self.sock.send_multipart(['B_CLIENT', self.message])
                        self.message = None
                elif sender == 'B_CLIENT':
                    # print sender
                    # print self.message
                    # self.sock.send_multipart(['GUI', self.message])
                    print '{0}:{1}'.format('q2', self.message)
                    self.message = None

    def join(self, timeout=None):
        self.stoprequest.set()
        super(Router, self).join(timeout)

import zmq
import threading
from constants import *

class Client(threading.Thread):
    def __init__(self, threadID, name, ctx):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.stoprequest = threading.Event()

        self.context = ctx
        self.dealer = self.context.socket(zmq.DEALER)
        self.dealer.identity = 'W_CLIENT'
        self.pull = self.context.socket(zmq.PULL)
        self.push = self.context.socket(zmq.PUSH)

        self.dealer.connect(TCP_ADDR)
        self.pull.bind(SEND_ADDR) # try connect
        self.push.bind(RECV_ADDR)

        self.poller =zmq.Poller()
        self.poller.register(self.dealer, zmq.POLLIN)
        self.poller.register(self.pull, zmq.POLLIN)

    def run(self):
        while not self.stoprequest.is_set():
            socks = dict(self.poller.poll(1000))
            # message received from server
            if self.dealer in socks:
                tprint('test')
                msg = self.dealer.recv()
                tprint("{0}:{1}".format('recv from server',msg))
                self.push.send_string(msg)
            # message to be sent to server
            if self.pull in socks:
                msg = self.pull.recv_string()
                tprint("{0}:{1}".format('pull from inproc', msg))
                self.dealer.send_string(msg)

        self.dealer.close()
        self.push.close()
        self.pull.close()
        # self.context.term()

    def join(self, timeout=None):
        self.stoprequest.set()
        super(Client, self).join(timeout)

class Buffer(threading.Thread):
    def __init__(self, threadID, name, ctx):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.stoprequest = threading.Event()

        self.context = ctx
        self.dealer = self.context.socket(zmq.DEALER)
        self.dealer.identity = 'B_CLIENT'
        self.pull = self.context.socket(zmq.PULL)
        self.push = self.context.socket(zmq.PUSH)

        self.dealer.connect(IPC_ADDR)
        self.push.connect(SEND_ADDR) # try connect
        self.pull.connect(RECV_ADDR)

        self.poller =zmq.Poller()
        self.poller.register(self.dealer, zmq.POLLIN)
        self.poller.register(self.pull, zmq.POLLIN)

    def run(self):
        while not self.stoprequest.is_set():
            socks = dict(self.poller.poll(1000))
            # message received from ipc-router
            if self.dealer in socks:
                tprint('test')
                msg = self.dealer.recv()
                if msg == 'WINDOWCLOSED':
                    pass
                else:
                    tprint("{0}:{1}".format('recv from ipc-touter',msg))
                    self.push.send_string(msg) #send_addr
            # message to be sent to server
            if self.pull in socks:
                msg = self.pull.recv_string() #recv_addr
                tprint("{0}:{1}".format('pull from inproc', msg))
                self.dealer.send_string(msg) #send back to ipc

        self.dealer.close()
        self.push.close()
        self.pull.close()
        # self.context.term()

    def join(self, timeout=None):
        self.stoprequest.set()
        super(Client, self).join(timeout)

import zmq
import threading
from constants import *


class IPCDealer:
    def __init__(self, context):
        # Socket to talk to router
        self.context = context
        self.in_sock = self.context.socket(zmq.DEALER)
        self.in_sock.identity = 'web-dealer'
        self.in_sock.setsockopt(zmq.LINGER, 0)
        self.in_sock.connect(IPC_ADDR)
        # self.poller = zmq.Poller()
        # self.poller.register(self.in_sock, zmq.POLLIN)

    def close(self):
        self.in_sock.close()


class TCPDealer:
    def __init__(self, context):
        self.context = context
        self.out_sock = self.context.socket(zmq.DEALER)
        self.out_sock.identity = "tcp-dealer"
        self.out_sock.setsockopt(zmq.LINGER, 0)
        self.out_sock.connect(TCP_ADDR)
        # self.poller = zmq.Poller()
        # self.poller.register(self.out_sock, zmq.POLLIN)

    def close(self):
        self.out_sock.close()


class Client2(threading.Thread):
    def __init__(self, threadID, name, tcp_dealer, ipc_dealer):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.stoprequest = threading.Event()
        self.ipc = ipc_dealer
        self.tcp = tcp_dealer

        self.poller = zmq.Poller()
        self.poller.register(self.ipc.in_sock, zmq.POLLIN)
        self.poller.register(self.tcp.out_sock, zmq.POLLIN)

    def run(self):
        while not self.stoprequest.is_set():
            tprint('poll')
            socks = dict(self.poller.poll(1000))

            # message to be sent to server
            if self.ipc.in_sock in socks: # and socks[self.ipc.in_sock] == zmq.POLLIN:
                msg = self.ipc.in_sock.recv()
                if msg == 'WINDOWCLOSED':
                    pass
                else:
                    tprint("{0}:{1}".format('To server', msg))
                    self.tcp.out_sock.send(msg)

            # message received from server
            if self.tcp.out_sock in socks:
                tprint("yes")
                targ, msg = self.tcp.out_sock.recv()
                tprint("{0}:{1} from {2}".format('Received', msg, targ))
                if msg == 'World!':
                    self.ipc.in_sock.send_string(msg)
        self.ipc.close()
        self.tcp.close()

    def join(self, timeout=None):
        self.stoprequest.set()
        super(Client2, self).join(timeout)


class Client(threading.Thread):
    def __init__(self, threadID, name, ctx):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.stoprequest = threading.Event()

        self.context = ctx
        self.dealer = self.context.socket(zmq.DEALER)
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
                i_d, msg = self.dealer.recv_multipart()
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


class Sender(threading.Thread):
    def __init__(self, threadID, name, ctx):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.stoprequest = threading.Event()

        self.context = ctx
        self.sender = self.context.socket(zmq.PUSH)
        self.ipc = self.context.socket(zmq.DEALER)

        self.ipc.identity = 'web-dealer'
        self.ipc.setsockopt(zmq.LINGER, 0)

        self.sender.connect(SEND_ADDR)
        self.ipc.connect(IPC_ADDR)

        self.poller = zmq.Poller()
        self.poller.register(self.ipc, zmq.POLLIN)

    def run(self):
        while not self.stoprequest.is_set():
            socks = dict(self.poller.poll(1000))
            if self.ipc in socks:  # and socks[self.ipc.in_sock] == zmq.POLLIN:
                msg = self.ipc.recv()
                if msg == 'WINDOWCLOSED':
                    pass
                else:
                    tprint("{0}:{1}".format('push to inproc', msg))
                    self.sender.send_string(msg)

        self.ipc.close()
        self.sender.close()
        # self.context.term()

    def join(self, timeout=None):
        self.stoprequest.set()
        super(Sender, self).join(timeout)


class Receiver(threading.Thread):
    def __init__(self, threadID, name, ctx):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.stoprequest = threading.Event()

        self.context = ctx  # zmq.Context()
        self.receiver = self.context.socket(zmq.PULL)
        # self.tcp = DEALER
        self.receiver.connect(RECV_ADDR)

        self.poller = zmq.Poller()
        self.poller.register(self.receiver, zmq.POLLIN)

    def run(self):
        while not self.stoprequest.is_set():
            socks = dict(self.poller.poll(1000))
            if self.receiver in socks:
                msg = self.receiver.recv()
                tprint(msg)
        self.receiver.close()
        # self.context.term()

    def join(self, timeout=None):
        self.stoprequest.set()
        super(Receiver, self).join(timeout)

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
        self.poller = zmq.Poller()
        self.poller.register(self.in_sock, zmq.POLLIN)

    def close(self):
        self.in_sock.close()


class TCPDealer:
    def __init__(self, context):
        self.context = context
        self.out_sock = self.context.socket(zmq.DEALER)
        self.out_sock.identity = "tcp-dealer"
        self.out_sock.setsockopt(zmq.LINGER, 0)
        self.out_sock.connect(TCP_ADDR)
        self.poller = zmq.Poller()
        self.poller.register(self.out_sock, zmq.POLLIN)

    def close(self):
        self.out_sock.close()


class Sender(threading.Thread):
    def __init__(self, threadID, name, tcp_dealer, ipc_dealer):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.stoprequest = threading.Event()

        self.tcp = tcp_dealer
        self.ipc = ipc_dealer

    def run(self):
        while not self.stoprequest.is_set():
            socks = dict(self.ipc.poller.poll(1000))
            if self.ipc.in_sock in socks and socks[self.ipc.in_sock] == zmq.POLLIN:
                msg = self.ipc.in_sock.recv()
                if msg == 'WINDOWCLOSED':
                    print 'q3'
                    return -1
                else:
                    print "{0}:{1}".format('To server', msg)
                    self.tcp.out_sock.send(msg)
                    # in_msg = self.out_sock.recv()
                    # print "{0}:{1}".format('From server', in_msg)
                    # self.dealer.in_sock.send(in_msg)
        self.tcp.close()
        self.ipc.close()

    def join(self, timeout=None):
        self.stoprequest.set()
        super(Sender, self).join(timeout)


class Receiver(threading.Thread):
    def __init__(self, threadID, name, tcp_dealer, ipc_dealer):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.stoprequest = threading.Event()

        # Socket to talk to server
        self.tcp = tcp_dealer
        self.ipc = ipc_dealer

    def run(self):
        while not self.stoprequest.is_set():
            print 'rec: wh'
            socks = dict(self.tcp.poller.poll(1000))
            if self.tcp.out_sock in socks and socks[self.tcp.out_sock] == zmq.POLLIN:
                'print yes'
                targ, msg = self.tcp.out_sock.recv_multipart()
                print "{0}:{1} from {2}".format('Received', msg, targ)
                if msg == 'World!':
                    self.ipc.in_sock.send_string(msg)

        self.tcp.close()
        self.ipc.close()

    def join(self, timeout=None):
        self.stoprequest.set()
        super(Receiver, self).join(timeout)

import signal

from app_gui import RootApp
from web_client import *
from router import Router  # zmq and threading


def signal_handler(signal, frame):
    raise SIGTERM_Received()


class App:
    def __init__(self):
        self.context = None
        self.threads = []
        self.ipc = None
        self.tcp = None

    def initializer(self):
        self.context = zmq.Context()
        self.ipc = IPCDealer(self.context)
        self.tcp = TCPDealer(self.context)

        self.threads = [
            Router(1, 'router', self.context),
            Sender(2, 'sender', self.tcp, self.ipc),
            Receiver(3, 'receiver', self.tcp, self.ipc),

        ]

        for th in self.threads:
            th.daemon = True
            th.start()

    def terminator(self):
        for th in self.threads:
            print th.name
            th.join(10)
        print 'ctx.term'
        # self.ipc.close()
        # self.tcp.close()
        self.context.term()

    def run(self):
        """
        main method
        :return: nothing
        """

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        self.initializer()

        try:
            app = RootApp()
            app.mainloop()
        except SIGTERM_Received:
            pass
        self.terminator()

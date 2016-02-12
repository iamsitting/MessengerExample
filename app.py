import signal

from app_gui import RootApp
from web_client import *
from router import Router  # zmq and threading
import time
import cli


def signal_handler(signal, frame):
    raise SIGTERM_Received()


class App:
    def __init__(self, gui=True):
        self.context = None
        self.threads = []
        self.ipc_s = None
        self.ipc_r = None
        self.tcp_s = None
        self.tcp_r = None
        self.gui = gui

    def initializer(self):
        self.context = zmq.Context()
        # self.ipc_s = IPCDealer(self.context)
        # self.ipc_r = IPCDealer(self.context)
        # self.tcp_s = TCPDealer(self.context)
        # self.tcp_r = TCPDealer(self.context)

        self.threads = [
            Router(1, 'router', self.context),
            Client(2, 'client', self.context),
            Buffer(3, 'buffer', self.context),
            #Sender(3, 'sender', self.context),
            #Receiver(4, 'receiver', self.context),
            #Client(2, 'client'),
        ]

        for th in self.threads:
            th.daemon = True
            time.sleep(2)
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
            if self.gui is True:
                app = RootApp()
                app.mainloop()
            else:
                c = cli.CliThread(5, 'cli')
                # c.start()
                c.mainloop()

        except SIGTERM_Received:
            pass
        if self.gui is True:
            app.destroy()
        else:
            c.destroy()
            # c.join(10)
        self.terminator()

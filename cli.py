import sys
import zmq
import threading
from constants import *
class CLIDealer:
    def __init__(self):
        self.context = zmq.Context().instance()
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.identity = "CLI"
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.connect(IPC_ADDR)

class CliThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.conn = CLIDealer()
        self.threadID = threadID
        self.name = name
        self.stoprequest = threading.Event()
    
    def run(self):
        auth = {'cds100':'5959'}
        raw_input("Press 'Enter' to continue...")
        uname = raw_input("Enter your username.")
        pw = raw_input("Enter your password.")

        if uname in auth.keys():
            if pw == auth[uname]:
                print("Enter Message")
                while not self.stoprequest.is_set():
                    msg = input("> ")
                    self.conn.socket.send_string(msg)
                    
        sys.exit(0)

    def join(self, timeout=None):
        self.stoprequest.set()
        super(CliThread, self).join(timeout)


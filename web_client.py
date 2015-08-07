import zmq
import threading

IPCADDR = "ipc:///tmp/router.ipc"
TCPADDR = "tcp://localhost:5555"

class RouterSocket():
	def __init__(self, context):
		# Socket to talk to router
		self.context = context
		self.in_sock = self.context.socket(zmq.DEALER)
		self.in_sock.identity = 'web-dealer'
		self.in_sock.setsockopt(zmq.LINGER, 0)
		self.in_sock.connect(IPCADDR)
		self.poller = zmq.Poller()
		self.poller.register(self.in_sock, zmq.POLLIN)
		

class Sender(threading.Thread):
	def __init__(self, threadID, name, context, dealer):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.context = context
		self.stoprequest = threading.Event()

		self.out_sock = self.context.socket(zmq.REQ)
		self.out_sock.identity = 'web-req'
		self.out_sock.setsockopt(zmq.LINGER, 0)
		self.out_sock.connect(TCPADDR)
		self.dealer = dealer
		
	def run(self):
		while not self.stoprequest.is_set():
			socks = dict(self.dealer.poller.poll(1000))
			if self.dealer.in_sock in socks and socks[self.dealer.in_sock] == zmq.POLLIN:
				msg = self.dealer.in_sock.recv()
				if msg == 'WINDOWCLOSED':
					print 'q3'
					self.dealer.in_sock.close()
					self.out_sock.close()
					return -1
				print "{0}:{1}".format('To server', msg)
				self.out_sock.send(msg)
				in_msg = self.out_sock.recv()
				print "{0}:{1}".format('From server', in_msg)
				self.dealer.in_sock.send(in_msg)
	
	def join(self, timeout=None):
		self.stoprequest.set()
		super(Sender, self).join(timeout)

class Receiver(threading.Thread):
	def __init__(self, threadID, name, context, dealer):
		threading.Thread.__init__(self)
		self.stoprequest = threading.Event()
		
		# Socket to talk to server
		self.client_sock = context.socket(zmq.PULL)
		self.client_sock.identity = 'web-pull'
		self.client_sock.setsockopt(zmq.LINGER, 0)
		self.client_sock.connect(TCPADDR)
		self.dealer = dealer
	
	def run(self):
		while not self.stoprequest.is_set():
			message = self.client_sock.recv()
			self.dealer.in_sock.send(message)
	
	def join(self, timeout=None):
		self.stoprequest.set()
		super(Receiver, self).join(timeout)

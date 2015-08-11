import app_gui
import threading
from web_client import *
import signal
import time
import zmq
from router import Router

IPCADDR = "icp:///tmp/router.ipc"

class SIGTERM_Received(Exception):
	pass

def signal_handler(signal, frame):
	raise SIGTERM_Received()
	
class Gui(threading.Thread):
	def __init__(self, threadID, name, context):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.context = context
		self.stoprequest = threading.Event()
		self.exitThread = False
	
	def run(self):
		try:
			gui = app_gui.run()
			while not self.stoprequest.is_set():
				if gui.quitted is True:
					self.exitThread = True
					return -1
		except Exception as e:
			print e
			
	def join(self, timeout=None):
		self.stoprequest.set()
		super(Gui, self).join(timeout)

class App():
	def __init__(self):
		self.context = None
		self.threads = []
	
	def initializer(self):
		self.context = zmq.Context()
		self.ipc = IPCDealer(self.context)
		self.tcp = TCPDealer(self.context)
		
		self.threads = [
			Gui(1, 'gui', self.context),
			Sender(2, 'sender', self.tcp, self.ipc),
			Receiver(3, 'recv', self.tcp, self.ipc),
		]
		
		for th in self.threads:
			th.daemon = True
			th.start()
	
	def terminator(self):
		for th in self.threads:
			print th.threadID
			th.join(10)
		print 'ctx.term'
		#self.ipc.close()
		#self.tcp.close()
		self.context.term()
			
	def run(self):
		signal.signal(signal.SIGINT, signal_handler)
		signal.signal(signal.SIGTERM, signal_handler)
		try:
			
			self.initializer()
			while True:
				time.sleep(1)
				
				if self.threads[0].exitThread == True:
					raise SIGTERM_Received()
		except SIGTERM_Received:
			pass
		self.terminator()

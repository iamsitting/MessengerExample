import Tkinter as tk
import tkMessageBox as mb
import zmq
from pyframes import *

IPCADDR = "ipc:///tmp/router.ipc"
LARGE_FONT = ("Verdana", 12)
worker = None

class connection():
	def __init__(self):
		global worker
		context = zmq.Context().instance()
		worker = context.socket(zmq.DEALER)
		worker.identity = "GUI"
		worker.setsockopt(zmq.LINGER, 0)
		worker.connect(IPCADDR)
	

class App(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.quitted = False
		container = tk.Frame(self) #parent frame
		
		container.pack(side="top", fill="both", expand=True)
		
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		
		self.frames = {}
		
		for fr in (StartPage, Login, Messenger, Register):
			frame = fr(container, self)
			self.frames[fr] = frame
			frame.grid(row=0, column=0, sticky="nsew")
		
		self.show_frame(StartPage)
	
		self.protocol('WM_DELETE_WINDOW', self.OnWindowClose)
		
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise() #bring frame to top
	
	def SendMessage(self, message):
		worker.send_string(message)
	
	def OnWindowClose(self):
		#pass message to App
		if mb.askokcancel("Quit", "Do you want to quit?"):
			self.SendMessage('WINDOWCLOSED')
			worker.close()
			self.quitted = True
			self.quit()
def run():
	conn = connection()
	app = App() #First GUI has no parent
	app.mainloop()
	return app
	
if __name__ == '__main__':
	run()

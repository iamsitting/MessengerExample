import Tkinter as tk
import tkMessageBox as mb

class Register(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.cont = controller
		
		self.grid()
		self.label1 = tk.Label(self, text="Username")
		self.label2 = tk.Label(self, text="Password")
		self.label3 = tk.Label(self, text="Confirm")
		
		self.entry1 = tk.Entry(self)
		self.entry2 = tk.Entry(self)
		self.entry3 = tk.Entry(self)
		
		self.label1.grid(row=0, sticky="W")
		self.label2.grid(row=1, sticky="W")
		self.label3.grid(row=2, sticky="W")
		
		self.entry1.grid(row=0, column=1, sticky = "EW")
		self.entry2.grid(row=1, column=1, sticky = "EW")
		self.entry3.grid(row=2, column=1, sticky = "EW")

class Login(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.loggedin = False
		self.cont = controller
	
		self.grid()
		print '2'
		self.label1 = tk.Label(self, text="Username")
		self.label2 = tk.Label(self, text="Password")
		print '2'
		self.entry1 = tk.Entry(self)
		self.entry2 = tk.Entry(self)
		
		self.label1.grid(row=0, sticky='W')
		self.label2.grid(row=1, sticky='W')
		self.entry1.grid(row=0, column=1, sticky = "Ew")
		self.entry2.grid(row=1, column=1, sticky = "EW")
		#label.grid(column=0, row=1, columnspan=2, sticky='EW')
		self.checkbox = tk.Checkbutton(self, text="Keep me logged in")
		self.checkbox.grid(columnspan=2)
		
		self.logbtn = tk.Button(self, text="Login", command = self.OnLoggedInButtonClick)
		self.logbtn.grid(columnspan=2)
		
		self.regbtn = tk.Button(self, text="Register", command = lambda: self.cont.show_frame(Register))
		self.regbtn.grid(columnspan=2)
		#self.grid_columnconfigure(0, weight=1) #resize column 0
		#self.cont.resizable(False,False) #prevents vertical resizing
		#self.update()
		#self.cont.geometry(self.cont.geometry()) #prevents auto-sizing
		
	def OnLoggedInButtonClick(self):
		uname = self.entry1.get()
		pw = self.entry2.get()
		
		if uname == 'cds100' and pw == '5959':
			self.loggedin = True
			self.cont.show_frame(Messenger)
		else:
			self.loggedin = False
			mb.showerror("Login Error", "Invalid username or password")

class Messenger(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)	
		self.quitted = False
		self.cont = controller
		self.hist_count = 0
		
		self.grid() #Tk grid layout manager
		
		self.entryVariable = tk.StringVar()
		self.entry = tk.Entry(self,#creates Entry widget
									textvariable=self.entryVariable)
									
		self.entry.grid(column=0, row=0, sticky='EW') #adds widget
		#when return is entered, call self.OnPressEnter
		self.entry.bind("<Return>", self.OnPressEnter) #bind widget
		self.entryVariable.set(u'Enter text here')
		
		#when button is clicked, call OnButtonClick
		button = tk.Button(self, text=u"Click me !",
								command=self.OnButtonClick)
		button.grid(column=1, row=0)
		
		self.labelVariable = tk.StringVar()
		label = tk.Label(self,
						textvariable=self.labelVariable,
						anchor='w', #west aligned
						fg='white', #white text
						bg='blue') #blue background
		label.grid(column=0, row=1, columnspan=2, sticky='EW')
		self.labelVariable.set(u'Hello')
		
		self.grid_columnconfigure(0, weight=1) #resize column 0
		self.cont.resizable(True,False) #prevents vertical resizing
		self.update()
		self.cont.geometry(self.cont.geometry()) #prevents auto-sizing
		self.entry.focus_set() #focus on entry
		self.entry.selection_range(0, tk.END) # select all
		
	def UpdateHistory(self, message):
		self.hist_count = self.hist_count + 1
		labvar = tk.StringVar()
		label = tk.Label(self,
						textvariable=labvar,
						anchor='w', #west aligned
						fg='white', #white text
						bg='blue') #blue background
		label.grid(column=0, row=self.hist_count, columnspan=2, sticky='EW')
		labvar.set(message)
		self.grid_columnconfigure(0, weight=1) #resize column 0
		self.cont.resizable(True,False) #prevents vertical resizing
		self.update()
		self.cont.geometry(self.cont.geometry()) #prevents auto-sizing
		
	def OnButtonClick(self):
		input = self.entryVariable.get()
		print "From user: {0}".format(input)
		#self.labelVariable.set(input +" (via button)")
		self.UpdateHistory(input)
		self.entry.focus_set()
		self.entry.selection_range(0, tk.END)
		self.cont.SendMessage(input)
		
	def OnPressEnter(self, event): #event comes from bind
		self.OnButtonClick()

class StartPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Start Page")
		label.pack(pady=10, padx=10)
		button = tk.Button(self, text="Login",
							command = lambda: controller.show_frame(Login))
		button.pack()

class ScrollTextArea(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.cont = controller

		self.text = tk.Text(self, height = 50, width = 90)
		scroll = tk.Scrollbar(self)
		self.text.configure(yscrollcommand=scroll.set)
		
		self.text.pack(side=LEFT)
		scroll.pack(side=RIGHT, fill=Y)
		self.pack(side=TOP)

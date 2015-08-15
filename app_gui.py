import zmq
from pyframes import *  # imports tk
from constants import *

worker = None


class GUIDealer:
    def __init__(self):
        self.context = zmq.Context().instance()
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.identity = "GUI"
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.connect(IPC_ADDR)


class RootApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.conn = GUIDealer()
        self.quitted = False
        self.grid()

        container = tk.Frame(self)  # parent frame

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for fr in (StartPage, Login, Messenger, Register):
            frame = fr(container, self)
            self.frames[fr] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
        self.protocol('WM_DELETE_WINDOW', self.on_window_close)

    def show_frame(self, cont):
        print 'show_frame'
        frame = self.frames[cont]
        try:
            frame.show()
            frame.tkraise()  # bring frame to top

            # frame.grid(row=0, column=0, sticky="nsew")
            print 'raised'
        except Exception as e:
            print e

    def send_message(self, message):
        self.conn.socket.send_string(message)

    def on_window_close(self):
        # pass message to App
        if mb.askokcancel("Quit", "Do you want to quit?"):
            self.send_message('WINDOWCLOSED')
            self.conn.socket.close()
            self.quitted = True
            self.quit()
            raise SIGTERM_Received


def run():  # root tester
    app = RootApp()  # First GUI has no parent
    app.mainloop()
    return app

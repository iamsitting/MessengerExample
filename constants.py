IPC_ADDR = "ipc:///tmp/router.ipc"
TCP_ADDR = "tcp://localhost:5555"
LARGE_FONT = ("Verdana", 12)


class PROC_ID:
    GUI = "GUI"
    ROUTER = "ROUTER"
    TCP_CLIENT = "TCP_CLIENT"


class SIGTERM_Received(Exception):
    pass

import sys

IPC_ADDR = "ipc:///tmp/router.ipc"
TCP_ADDR = "tcp://localhost:5555"
SEND_ADDR = "inproc://send"
RECV_ADDR = "inproc://recv"
LARGE_FONT = ("Verdana", 12)


class PROC_ID:
    GUI = "GUI"
    ROUTER = "ROUTER"
    TCP_CLIENT = "TCP_CLIENT"


class SIGTERM_Received(Exception):
    pass


def tprint(str):
    sys.stdout.write(str + '\n')
    sys.stdout.flush()
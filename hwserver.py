import zmq

context = zmq.Context()
socket = context.socket(zmq.ROUTER)
socket.identity = 'server'
socket.bind("tcp://*:5555")

poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)
message = None

while True:
    #  Wait for next request from client
    socks = dict(poller.poll(1000))
    if socket in socks and socks[socket] == zmq.POLLIN:
        sender, message = socket.recv_multipart()
        if message is not None:
            print '{0}:{1}'.format(sender, message)
            message += 'world'
            socket.send_string(message)
            socket.send_multipart([sender, message])
            message = None

#! /home/cds100/Projects/app/env/bin/python2.7
# -*- coding: iso-8859-1 -*-

import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.ROUTER)
socket.identity = 'server'
socket.bind("tcp://*:5555")


poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)

while True:
    #  Wait for next request from client
    
    
	socks = dict(poller.poll(1000))
	if (socket in socks and socks[socket] == zmq.POLLIN):
		sender, message = socket.recv_multipart()
			
		if message is not None \
		and sender == 'web-dealer':
	
			print '{0}:{1}'.format('server', message)
			socket.send_multipart(['web-dealer', "Word!"])
			message = None

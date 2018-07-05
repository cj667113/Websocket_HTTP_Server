import socket
import os
from websocket_server import WebsocketServer
import time
import threading
import base64
def http_server():
	addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
	s = socket.socket()
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(addr)
	s.listen(5)
	print('listening on', addr)
	while True:
		c1, addr = s.accept()
        	print repr(c1.recv(4096))
        	print('client connected from',addr)
		data = open("index.html", 'rb')
		data = data.read()
        	c1.send(data)
		time.sleep(.01)
       		c1.close()

def websocket_server():
	with open("thermal.jpg", "rb") as image_file:
		thermal=base64.b64encode(image_file.read())
	# Called for every client connecting (after handshake)
	def new_client(client, server):
	        print("New client connected and was given id %d" % client['id'])
	#       server.send_message_to_all("Hey all, client(%d) has joined us" % client['id'])
		while True:
			try:
				with open("thermal.jpg", "rb") as image_file:
					thermal=base64.b64encode(image_file.read())
				time.sleep(.015)
				server.send_message_to_all(thermal)
				time.sleep(.025)
			except:
				pass
	# Called for every client disconnecting
	def client_left(client, server):
	        print("Client(%d) disconnected" % client['id'])
		#server.send_message_to_all("Hey all, client(%d) had disconnected" % client['id'])

	# Called when a client sends a message
	def message_received(client, server, message):
	        if len(message) > 200:
	                message = message[:200]+'..'
	        print("Client(%d) said: %s" % (client['id'], message))

	PORT=9876
	server = WebsocketServer(PORT,host="0.0.0.0")
	server.set_fn_new_client(new_client)
	server.set_fn_client_left(client_left)
	server.set_fn_message_received(message_received)
	server.run_forever()

threading.Thread(target=websocket_server).start()
threading.Thread(target=http_server).start()

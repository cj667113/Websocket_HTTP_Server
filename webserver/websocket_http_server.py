import socket
from websocket_server import WebsocketServer
import time
import threading

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

        	c1.send(
        	'''<!DOCTYPE html>
        	<html xmlns="http://www.w3.org/1999/xhtml">
        	  <head>
        	    <title>Web Socket Example</title>
        	    <meta charset="UTF-8">
        	    <script>
        	      window.onload = function() {
        	        var s = new WebSocket("ws://10.101.5.206:9876/");
        	        s.onopen = function(e) { alert("opened"); }
        	        s.onclose = function(e) { alert("closed"); }
        	        s.onmessage = function(e) { alert("got: " + e.data); }
        	      };
        	    </script>
        	  </head>
        	<body>
        	  <div id="holder" style="width:600px; height:300px"></div>
        	</body>
        	</html>''')

        	time.sleep(.01)
       		c1.close()

def websocket_server():
	# Called for every client connecting (after handshake)
	def new_client(client, server):
	        print("New client connected and was given id %d" % client['id'])
	        server.send_message_to_all("Hey all, a new client has joined us")

	# Called for every client disconnecting
	def client_left(client, server):
	        print("Client(%d) disconnected" % client['id'])

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

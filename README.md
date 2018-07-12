# Websocket_HTTP_Server
Websocket_HTTP_Server is a collection of files that will easily display a set of data being gathered over a web browser, the collection was originally built to display thermal images over http/tcp port 80 in a real-time fashion. When connecting to the http server, the server delieves index.html that will launch a javascript program on load. This program connects to the websocket server, where the websocket server pushes data down to all the clients.

This program is uses the package from [python-websocket-server](https://github.com/Pithikos/python-websocket-server), which I installed using sudo pip install websocket-server.Furthermore, in the /usr/local/lib/python2.7/dist-packages/websocket_server the python program websocket_server.py is installed. I edited this file and commented out line 207, which is responsible for the error message "Can't send message, message is not valid UTF-8", because when opening the image that another thread is still writing to, there will an incomplete file that is read. The error message will not break the program I wrote, but will spam the command line.

![alt-text](https://raw.githubusercontent.com/cj667113/Websocket_HTTP_Server/master/Img/Web_socket_error_message_spam.jpg)

By running websocket_http_server.py, the python program will startup an http server and a websocket server which will pull configuration settings from server.conf which also has a file path to the image that will be constantly sent in a loop. The program will encode thermal.jpg into a base64 format and sent it over the websocket connection.

shift.sh is a shell script that copies thermal2-thermal4.jpg into thermal.jpg which will be displayed. You will need to run sudo chmod u+x shift.sh and run it as root, we used this as a test to ensure that the stream of data was running to the clients by shuffling the images into thermal.jpg.

index.html is server by the http server, which onload will hook into the websocket server. index.html will collect the data that is being streamed from the websocket server and display it as an image by decoding the image and placing it on the web browser. index.html handles the formating of the image in terms of the dimensions that it will be displayed as.

server.conf is the configuration file that websocket_http_server.py will use in order to determine that port and interface numbers that the servers will broadcast on.

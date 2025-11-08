'''
Basics of server.py from Amy Csizmar Dalal CS331 Networks Fall 2025
https://github.com/acdalal/cs331-gopher/blob/main/gopherServer.py


Create server! Print any input taken! 

'''

import sys, socket
DEFAULT_PORT = 48939
SERVER_PRIVATE = "server private key :)"

def listen(serverSocket):
	serverSocket.listen(5)

	while True:
		clientSock, clientAddr = serverSocket.accept()
		print("Connection received from ",  clientSock.getpeername())
		while True:
			try: 
				data = clientSock.recv(1024)
			except:
				break

			if not len(data):
				break

			try:
				decoded = data.decode("ascii")
			except:
				decoded = "COULD NOT DECODE"

			print("Received message:  " + decoded)

		clientSock.close()
		print("CLOSED!")

def create_server(port):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# the "" is the host, we don't care about the name because we're doing stuff
	# by IP addresses
	server.bind(("", port))
	return server


def main():
	server = create_server(DEFAULT_PORT)
	print("The server is running! It is at port", DEFAULT_PORT)
	listen(server)

main()
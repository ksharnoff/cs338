'''
basickeylogger.py
Kezia Sharnoff

Used in demo video
'''

# From page: https://pynput.readthedocs.io/en/latest/keyboard.html#monitoring-the-keyboard

from pynput import keyboard

def on_press(key):
	output = None
	try:
		output = format(key.char)
	except AttributeError:
		output = format(key)
		
	print(output)

with keyboard.Listener(
		on_press = on_press) as listener:
	listener.join()

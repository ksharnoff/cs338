# Keylogger Project

Kezia Sharnoff, CS338 Computer Security, November 12, 2025


## What happens from a user's view? 

0. Control and command server starts, `python3 server.py`
1. User downloads the `party_schedule` file from a phishing email
2. User double clicks the `party_schedule` file which does the following:
	1. Creates an executable `keyLogger` and runs it 
		- This process also creates a terminal window with a finished process, this system with the finished process is the best I was able to do on MacOS using `pyinstaller`. I imagine some users will not mind this window. 
		- The executable only needs Terminal to have the permission `Input Monitoring`. Some users likely already have this enabled, and others may need to click to enable (using administrator password) in system settings. 
	2. Creates a file named `cake_schedule.png` and opens it using the operating system's default image opening software
	3. Deletes the original `party_schedule` executable
	4. Creates a `keylogger_config` file that has the server address, the user can edit this to change the address (wait at least one minute for it to change)
3. All keys that the user types will be sent to the server! This process will persist after the user turns off their computer (although it will not capture the keys typed while the computer is off)
4. In order to close the keylogger, users can either:
	* `ps aux | grep keylogger` and kill the process ID(s)
	* On activity monitor, search for `keylogger`, and click the process(es) and then the X at the top 


## What happens with the files and over the network? 

0. The server is listening on a specified port (`python3 server.py`)
1. User types a key, which the keylogger detects and appends to a file named `keylogged.txt`
2. With every key, there is a 1/50 chance that the following steps happen:
	1. The entire `keylogged.txt` file is read and deleted
	2. A new TCP connection to the server is created, the inputted keys are sent, the connection is closed


## To make a new executable: 

The following modules must be installed:
* `pyinstaller`
* `pynput`

All of the following steps should be done while in `project/user`
1. `pyinstaller --onefile keylogger.py`
2. Get the base64 version of that executable by `base64 -i dist/keylogger > ./keylogger64`
3. Copy the `keylogger64` into the `content` variable in `runner.py`
4. `pyinstaller --onefile runner.py`
5. Rename `runner` to `party_schedule`
5. Run the keylogger double clicking the `runner` executable!

It is currently compiled to run on MacOS. If you would like a `runner` executable on any other operating system, you can copy the above steps. Note that line `os.system("open ./cake_schedule.png")` in `runner.py` should be changed, for example on Linux it should be `os.system("xdg-open cake_schedule.png")`. 


## How to run without any executables (and no cake schedule picture)?

The following module must be installed:
* `pynput`

0. Start the server, `python3 project/server/server.py`
1. In the `project/user/` directory, create a file named `keylogger_config` with the IP address or hostname of the server
2. Run the keylogger `python3 project/user/keylogger.py`
3. To stop the keylogger and server, you can do `CTL + C` in their terminal windows


## Future expansion
1. Run it over UDP (If we get enough volume of keys, we don't care about reliability as much)
2. Encrypt the in transit data 

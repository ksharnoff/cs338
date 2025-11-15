# Keylogger Project

Kezia Sharnoff, CS338 Computer Security, November 12, 2025

## Note on November 14th

After the deadline passed, I realized that I forgot to submit a video demo. I also found an occasional problem with the TCP byte stream to Kali (in `client.py`) that can be fixed with two lines of code -- it already always worked on localhost (the many files changed is recompiling the executables). 

I have added this extra commit, which is late, because I think the video would be helpful if the executable or server cannot run. I know that assignments turned in late get a zero, please grade the assignment based on what I had turned in last night and if the executable doesn't work you can watch the video. All of the design information and explanations in the video are not new and are already written in this README.

Here is [my video demo](https://drive.google.com/file/d/1IUCyRxawrkA7u_DUdtRvgTyBm8htj6sK/view?usp=sharing) (any Carleton account can view). 


## Takeaways

* Main problem of a keylogger is how to get the user to start it running and to obtain the necessary permissions
* Running executables have a lot of access and control

## What happens from a user's view? 

0. Control and command server starts, `python3 server.py`
1. User downloads the `party_schedule` file from a phishing email
2. User double clicks the `party_schedule` file which does the following in the home (~/) directory:
	1. Creates an executable `keyLogger` and runs it 
		- This process also creates a terminal window with a finished process, this system with the finished process is the best I was able to do on MacOS using `pyinstaller`. I imagine some users will not mind this window. 
		- The executable only needs Terminal to have the permission `Input Monitoring`. Some users likely already have this enabled, and others may need to click to enable (using administrator password) in system settings. 
	2. Creates a file named `cake_schedule.png` and opens it using the operating system's default image opening software
	3. Creates a `keylogger_config` file that has the server address, port, and username the user can edit this to change any of the variables
3. All keys that the user types will be sent to the server! This process will persist after the user turns off their computer (although it will not capture the keys typed while the computer is off)
4. In order to close the keylogger, users can either:
	* `ps aux | grep keylogger` and kill the process ID(s)
	* On activity monitor, search for `keylogger`, and click the process(es) and then the X at the top 


## What happens with the files and over the network? 

0. The server is listening on a specified port (`python3 server.py`)
1. User types a key, which the keylogger detects and appends to a file named `client-keyslogged.txt`
2. With every key, there is a 1/50 chance that the following steps happen:
	1. The entire `client-keyslogged.txt` file is read and deleted
	2. A new TCP connection to the server is created:
		* An AES key encrypted with the server's public key is sent
		* The inputted keys encrypted with the AES key is sent
		* (Optionally) a username encrypted with AES is sent
		* The connection is closed
3. The inputted keys are written to a file, `username || server-keyslogged.txt` that is in the same directory as `server.py`

## To make a new executable: 

The following modules must be installed:
* `pyinstaller` (create an executable)
* `pynput` (keyboard input)
* `pycryptodome` (encryption)

All of the following steps should be done while in `project/user`
1. `pyinstaller --onefile keylogger.py`
2. Get the base64 version of that executable by `base64 -i dist/keylogger > ./keylogger64`
3. Copy `keylogger64` into the `content` variable in `runner.py`
4. `pyinstaller --onefile runner.py`
5. Rename `runner` to `party_schedule`
5. Run the keylogger double clicking the `party_schedule` executable, anywhere!

I am having the `runner` executable run the `keylogger` executable because this makes the system settings only ask for Terminal having input access, not `keylogger` having input access. In addition, this lets me run the process using `nohup`, which will persist after terminal and the computer closes. 

It is currently compiled to run on MacOS. If you would like a `runner` executable on any other operating system, you can copy the above steps. Note that line `os.system("open ./cake_schedule.png")` in `runner.py` should be changed, for example on Linux it should be `os.system("xdg-open cake_schedule.png")`. 


## How to run without any executables (and no cake schedule picture)?

The following module must be installed:
* `pynput` (keyboard input)
* `pycryptodome` (encryption)

0. Start the server: `python3 project/server/server.py`
1. Run the keylogger: `python3 project/user/keylogger.py`
2. Edit the `keylogger_config` to make the port and server name match the server running
3. To stop the keylogger and server, you can do `CTL + C` in their terminal windows


## Future expansion
1. Run it over UDP (If we get a high volume of keys, we don't care about reliability as much)
2. Add a hash to the in transit data to make sure all of it arrived


## Major Sources of Code (smaller sources cited inline)

* [AES code example from pycryptodome documentation](https://www.pycryptodome.org/src/examples#encrypt-data-with-aes) used in `encrypt.py`, `client.py`, `server.py`
* [Basic TCP server/client conversation from Amy Csizmar Dalal CS331 Computer Networks](https://github.com/acdalal/cs331-gopher/blob/main/gopherClient.py) used in `server.py` and `client.py`
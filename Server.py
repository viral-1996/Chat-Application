"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
	"""Sets up handling for incoming clients."""
	while True:
		client, client_address = SERVER.accept()
		print("%s:%s has connected." % client_address)
		client.send("Greetings from the cave! Now type your name and press enter!".encode("utf-8"))
		addresses[client] = client_address
		Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
	"""Handles a single client connection."""
	name = client.recv(BUFSIZ).decode("utf8")
	welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
	client.send(welcome.encode("utf-8"))
	msg = "%s has joined the chat!" % name
	broadcast(msg.encode("utf8"))
	clients[client] = name

	while True:
		msg = client.recv(BUFSIZ)
		if msg != "{quit}".encode("utf8"):
			broadcast(msg, name+": ")
		else:
			client.send("{quit}".encode("utf8"))
			msg = "%s has left the chat." % name
			broadcast(msg.encode("utf8"))
			client.close()
			del clients[client]
			break

def broadcast(msg, prefix=""):  
	"""Broadcasts a message to all the clients."""
	for sock in clients:
		sock.send(prefix.encode("utf8")+msg)


clients = {}
addresses = {}

HOST = ''
PORT = 27001
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
	SERVER.listen(5)
	print("Waiting for connection...")
	ACCEPT_THREAD = Thread(target=accept_incoming_connections)
	ACCEPT_THREAD.start()
	ACCEPT_THREAD.join()
	SERVER.close()

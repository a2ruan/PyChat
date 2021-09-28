
# Python program to implement server side of chat room.
import socket
import select
import sys
from threading import Thread


class Server(Thread):
	MAX_ACTIVE_CONNECTIONS = 100

	def __init__(self, ip_address, port):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		self.ip_address = ip_address
		self.port = port
		self.server.bind((self.ip_address, self.port))
		
		self.server.listen(self.MAX_ACTIVE_CONNECTIONS)
		self.list_of_clients = []

	def clientthread(self, connection, address):
	 
	    # sends a message to the client whose user object is conn
	    connection.send("Welcome to this chatroom!")
	 
	    while True:
	            try:
	                message = connection.recv(2048)
	                if message:
	 
	                    """prints the message and address of the
	                    user who just sent the message on the server
	                    terminal"""
	                    print ("<" + address[0] + "> " + message)
	 
	                    # Calls broadcast function to send message to all
	                    message_to_send = "<" + address[0] + "> " + message
	                    broadcast(message_to_send, connection)
	 
	                else:
	                    """message may have no content if the connection
	                    is broken, in this case we remove the connection"""
	                    remove(connection)
	 
	            except:
	                continue
 
	def broadcast(self, message, connection):
	    for clients in self.list_of_clients:
	        if clients!=connection:
	            try:
	                clients.send(message)
	            except:
	                clients.close()
	 
	                # if the link is broken, we remove the client
	                remove(clients)
 
	def remove(self, connection):
	    if connection in self.list_of_clients:
	        self.list_of_clients.remove(connection)
 


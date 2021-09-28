from server import *
from client import *
from threading import Thread

class ServerCluster(Thread):
	def __init__(self):
		super().__init__()
		self.server = Server('127.0.0.1',666)

	def run(self):
		while True:
			print("hello")
			connection, address = server.server.accept()
			server.list_of_clients.append(connection)
			print (address[0] + " connected")
			start_new_thread(clientthread,(connection,address))

	def destroy(self):
		self.connection.close()
		self.server.server.close()
		print("Server shut down")

class ClientCluster(Thread):
	def __init__(self):
		super().__init__()
		self.client = Client('127.0.0.2',666)

	def run(self):
		while True:
			self.sockets_list = [sys.stdin, self.client.server]
			read_sockets,write_socket, error_socket = select.select(self.sockets_list,[],[])
			for socks in read_sockets:
				if socks == self.client.server:
					message = socks.recv(2048)
					print (message)
				else:
					message = sys.stdin.readline()
					self.client.server.send(message)
					sys.stdout.write("<You>")
					sys.stdout.write(message)
					sys.stdout.flush()

	def destroy(self):
		self.server.close()


if __name__ == '__main__':
	chat_server = ServerCluster()
	client = ClientCluster()
	chat_server.start()
	client.start()
# Python program to implement client side of chat room.
import socket
import select
import sys

class Client():
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((self.ip_address, self.port))


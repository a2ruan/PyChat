import socket
import threading

class Client:
    def __init__(self):
        # Go to create_connection function 
        self.create_connection()

    def create_connection(self):
        # Initialize socket with IVP4 using TCP
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        while 1:
            try:
                host = input('Enter host name --> ')
                port = int(input('Enter port --> '))
                self.s.connect((host,port))
                
                break
            except:
                print("Couldn't connect to server")

        self.username = input('Enter username --> ')
        self.s.send(self.username.encode())
        # Initialize two seperate threads per Client to send and recieve messages
        # Initialize thread to recieve messages
        message_handler = threading.Thread(target=self.handle_messages,args=())
        message_handler.start()

        # Initialize thread to send messages
        input_handler = threading.Thread(target=self.input_handler,args=())
        input_handler.start()

    def handle_messages(self):
        # Print out any messages from the server
        while 1:
            print(self.s.recv(1204).decode())

    def input_handler(self):
        # Take user input and send messages constantly.  Server will display message if non-null
        while 1:
            self.s.send((self.username+' - '+input()).encode())

client = Client()
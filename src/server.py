import socket
import threading

class Server:
    def __init__(self):
        self.start_server()

    def start_server(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print(socket.gethostbyname(socket.gethostname()))
        host = socket.gethostbyname(socket.gethostname())

        port = int(input('Enter port to run the server on --> '))
        # Client list
        self.clients = []
        
        self.s.bind((host,port))
        self.s.listen(100)
    
        print('Running on host: '+str(host))
        print('Running on port: '+str(port))

        self.username_lookup = {}

        while True:
            # Check for new connections, where c = Client() and addr = address
            c, addr = self.s.accept()
            username = c.recv(1024).decode()
            
            print('New connection. Username: '+str(username))
            # Broadcast to all clients on server via instance function
            self.broadcast('New person joined the room. Username: '+username)
            # Append username to username list, and clients object to list
            self.username_lookup[c] = username
            self.clients.append(c)
            # Start a new thread to handle the client I/O
            threading.Thread(target=self.handle_client,args=(c,addr,)).start()

    # Send message to all clients via broadcast
    def broadcast(self,msg):
        for connection in self.clients:
            connection.send(msg.encode())


    def handle_client(self,c,addr):
        while True:
            try:
                # Recieve message from client
                msg = c.recv(1024)
            except:
                # When message cannot be recieved, shut down socket, remove from list
                c.shutdown(socket.SHUT_RDWR)
                self.clients.remove(c)
                # Broadcast message that user has left the room
                print(str(self.username_lookup[c])+' left the room.')
                self.broadcast(str(self.username_lookup[c])+' has left the room.')

                break
            # Broadcast to all clients other than sender if message is not blank
            if msg.decode() != '':
                print('New message: '+str(msg.decode()))
                for connection in self.clients:
                    if connection != c:
                        connection.send(msg)

server = Server()
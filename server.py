# These tutorials and forum posts have been used as sources:
# https://www.youtube.com/watch?v=3UOyky9sEQY
# https://stackoverflow.com/questions/54891425/how-to-make-a-kick-feature-in-python-socket-chat-room

import socket
import threading

clients = []
nicknames = []

# Define host and port
host = "127.0.0.1"
port = 8000

# Start server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Function to send message to all connected clients
def public_message(msg):
    for client in clients:
        client.send(msg)

# Function to handle messages from clients
# (and remove clients if needed)
def handle(client):
    while True:
        msg = client.recv(1024)
        public_message(msg)

# Receiving/listening function
def receive():
    while True:
        client, address = server.accept()
        print(address, "connected")

        # Ask for client's nickname and add client to list
        client.send("nickname".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        clients.append(client)
        nicknames.append(nickname)

        # Send info about the new chatter to other users
        public_message(nickname.encode("ascii"), "joined the chat!")
        client.send("Connected to server.".encode("ascii"))

        # Create a thread for the client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start

receive()

# These tutorials and forum posts have been used as sources:
# https://www.youtube.com/watch?v=3UOyky9sEQY
# https://stackoverflow.com/questions/54891425/how-to-make-a-kick-feature-in-python-socket-chat-room

import socket
import threading

clients = []
nicknames = []

host = "127.0.0.1"
port = 8000
print("Listening on port 8000")

# Start server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Function to send message to all connected clients
def public_message(msg):
    for client in clients:
        client.send(msg)

# Send message to one client
def private_message(msg):
    for client in clients:
        idx = clients.index(client)
        if ("//pm " + nicknames[idx]) in msg:
            msg = msg.replace("//pm " + nicknames[idx], "[pm]")
            client.send(msg.encode("ascii"))

# Function to handle messages from clients
# (and remove clients if needed)
def handle(client):
    while True:
        try:
            msg = client.recv(1024).decode("ascii")
            if "//quit" in msg:
                print("quit")
                remove(client)
                break
            elif "//pm" in msg:
                print("pm")
                private_message(msg)
            else:
                public_message(msg.encode("ascii"))
        except:
            remove(client)
            print(clients)
            break

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
        client.send("Connected to server.\n".encode("ascii"))
        msg = nickname + " joined the chat!\n"
        public_message(msg.encode("ascii"))

        # Create a thread for the client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Function to remove a client
def remove(client):
    if client in clients:
        idx = clients.index(client)
        clients.remove(client)
        client.close()
        print(nicknames[idx], "disconnected")
        public_message(("{} left the chat.\n".format(nicknames[idx])).encode("ascii"))
        del nicknames[idx]

receive()

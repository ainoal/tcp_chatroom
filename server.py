######################################################################
# Server program for Distributed Systems course
# Assignment 3
# server.py
# Author: ainoal
######################################################################
# These tutorials and forum posts have been used as sources:
# https://www.youtube.com/watch?v=3UOyky9sEQY
# https://www.geeksforgeeks.org/simple-chat-room-using-python/
# https://stackoverflow.com/questions/54891425/how-to-make-a-kick-feature-in-python-socket-chat-room
######################################################################

import socket
import threading

clients = []
nicknames = []
channels = []

host = "127.0.0.1"
port = 8000
print("Listening on port 8000")

# Start server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Receiving/listening function
def receive():
    while True:
        client, address = server.accept()
        print(address, "connected")

        # Ask for client's nickname and add client to list
        client.send("nickname".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        if nickname in nicknames:
            client.send(("Nickname already taken, please try again.").encode("ascii"))
            client.send("exit".encode("ascii"))
        else:
            client.send("channel".encode("ascii"))
            channel = client.recv(1024).decode("ascii")
            clients.append(client)
            nicknames.append(nickname)
            channels.append(channel)

            # Send info about the new chatter to other users
            client.send("Connected to server.\n".encode("ascii"))
            msg = nickname + " joined the chat!\n"
            public_message(msg.encode("ascii"), channel)

            # Create a thread for the client
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()

# Handle messages from clients (and remove clients if needed)
def handle(client):
    idx = clients.index(client)
    channel = channels[idx]
    while True:
        try:
            msg = client.recv(1024).decode("ascii")
            if "//quit" in msg:
                remove(client)
                break
            elif "//pm" in msg:
                private_message(msg, client)
            elif "//channel" in msg:
                channel = msg.replace((nicknames[idx] + ": //channel "), "")
                channels[idx] = channel
                public_message(("{} joined the channel!".format(nicknames[idx])).encode("ascii"), channel)
            elif "//active" in msg:
                get_active_users_and_channels(client)
            else:
                public_message(msg.encode("ascii"), channel)
        except:
            remove(client)
            break

# Send a message to all connected clients
def public_message(msg, channel):
    for client in clients:
        idx = clients.index(client)
        if channels[idx] == channel:
            client.send(msg)

# Send a private message to one client
def private_message(msg, sender):
    message_sent = False
    for client in clients:
        idx = clients.index(client)
        if ("//pm " + nicknames[idx]) in msg:
            msg = msg.replace("//pm " + nicknames[idx], "[pm]")
            client.send(msg.encode("ascii"))
            message_sent = True
    if message_sent == False:
        sender.send("No active user with the specified nickname :(".encode("ascii"))

# Remove a client
def remove(client):
    if client in clients:
        idx = clients.index(client)
        clients.remove(client)
        client.close()
        nickname = nicknames[idx]
        channel = channels[idx]
        print(nickname, "disconnected")
        public_message(("{} left the chat.\n".format(nickname)).encode("ascii"), channel)
        del nicknames[idx]
        del channels[idx]
        client.send("exit")

# Send client the information of active users and channels
def get_active_users_and_channels(requester):
    string = "Other active users:\n"
    for client in clients:
        idx = clients.index(client)
        if client != requester:
            string = string + nicknames[idx] + "\n"
    string = string + "Active channels:\n"
    allchannels = []
    for channel in channels:
        if channel not in allchannels:
            allchannels.append(channel)
            string = string + channel + "\n"
    requester.send(string.encode("ascii"))

receive()

######################################################################
# eof

######################################################################
# Client program for Distributed Systems course
# Assignment 3
# client.py
# Author: ainoal
######################################################################

import socket
import threading
import sys

nickname = input(" Choose a nickname: ")
channel = input("Write the name of the channel you want to join: ")

# Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 8000))

# Listen to server
def receive():
    while True:
        try:
            msg = client.recv(1024).decode("ascii")
            if (msg == "nickname"):
                client.send((nickname).encode("ascii"))
            elif (msg == "channel"):
                client.send((channel).encode("ascii"))
            elif (msg == "exit"):
                print("Nickname already taken, please try again")
                sys.exit(0)
            else:
                print(msg)
        except:
            print("Error. Closing connection.\n")
            client.close()
            sys.exit(0)

# Send messages
def write_msg():
    while True:
        msg = "{}: {}".format(nickname, input(""))
        client.send(msg.encode("ascii"))

# Start threads for listening and writing
thread_receive = threading.Thread(target=receive)
thread_receive.start()
thread_write = threading.Thread(target=write_msg)
thread_write.start()

######################################################################
# eof

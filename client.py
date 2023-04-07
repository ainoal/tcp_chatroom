import socket
import threading

nickname = input(" Choose a nickname: ")

# Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 8000))

# Function to listen to server and choose a nickname
def receive():
    while True:
        msg = client.recv(1024).decode("ascii")
        if (msg == "nickname"):
            client.send((nickname).encode("ascii"))
        else:
            print(msg)

# Function to send massages to server
def write_msg():
    while True:
        msg = "{}: {}\n".format(nickname, input(""))
        client.send(msg.encode("ascii"))

# Start threads for listening and writing
thread_receive = threading.Thread(target=receive)
thread_receive.start()
thread_write = threading.Thread(target=write_msg)
thread_write.start()

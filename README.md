# Distributed Systems Assignment 3
## Multi-user chat system using TCP socket technology

This is a multi-user chat system developed for Distributed Systems course. The system uses TCP socket technology. The chat system supports multiple channels and private messages between users. When a user wants to connect to the server, they are first asked to enter a nickname and a channel that they want to enter.
After this, the user can start chatting with others on the same channel or write a private message to user that is connected to the server.

The system uses multithreading. Server creates a new thread for each client to handle all of them at the same time.

Clients have several options for messaging. If they just write text without any of the following commands, the client program will send the message to the server, which will again send it to every client in the same channel as the sender. Specific commands that a user can include in their message:

//quit                          Disconnect
//pm [another user’s name]      Private message
//channel [channel name]        Change to another chat channel
//active                        Get a list of other active users and active channels

If the message that the server receives from a client includes any of these commands, it will be processed accordingly.

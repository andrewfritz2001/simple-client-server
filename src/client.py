###################################################################################################
## Client for 1-1 messaging application with server
## Supports file transfers following a specific format
## Code largely taken from https://realpython.com/python-sockets/
###################################################################################################
## python3 client.py
## OR
## python3 server.py 127.0.0.1 4000
## where 127.0.0.1 can be any IP and 4000 can be any port 
###################################################################################################

import socket
import sys

# Server IP and port are arbitrary. Localhost used for convenience
HOST = "127.0.0.1" 
PORT = 65432  


def make_socket():
    """ Constructing and returning a socket to connect to the server
    """
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def collect_signature():
    """ Welcome prompt when the server first establishes a connection. 
    
    Gets the user's name and creates a signature so the server knows who's talking 

    """
    print("\nWelcome to the chatroom!")
    print("Please enter your name: ", end = '')
    name = input()
    signature = name + ": "
    return signature




sock = make_socket()
sock.connect((HOST, PORT))

signature = collect_signature()

while True:
    print(signature, end = '')
    message = input()
    sock.sendall(bytes(signature+message,'utf-8'))
    data = sock.recv(1024)
    print(data.decode('utf-8'))
    
sock.close()

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

import send_file
import recv_file
import threading
import socket
import select
import time
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
    
def file_rec():
    print("recieving file...")
    time.sleep(0.1)
    recv_file.start()
    print("file receieved!")

def file_send(sock,path):
    print('sending file...')
    sock.sendall(bytes("[]","utf-8"))
    send_file.start(path)
    print('file sent!')
    
    
def rec_data(sock):
    """ Function to be targeted by async thread to always listen for incoming messages 
    """
    while True:
        rlist, wlist, xlist = select.select([sock],[sock],[])
        for sock in rlist:
            data = sock.recv(1024)
            if not data:
                raise Exception("We have a problem w client recv")
            if data ==b"[]":
                file_rec()
            else:
                print(data.decode('utf-8'))

def message_sends_file(message):
    """ Returns true if a mesage is encased in closed brackets
    """
    if len(message) < 2:
        return False
    return True if message[0] == '[' and message[-1] == ']' else False

def send_data(sock,signature):
    """ Function to be targeted by main thread and send data
    """
    while True:
        message = input()
        if message_sends_file(message):
            path = message[1:-1]
            file_send(sock,path)
        else:
            sock.sendall(bytes(signature+message,'utf-8'))

def start():
    """ Function to asynchronously send and recieve messages
    """
    sock = make_socket()
    sock.connect((HOST, PORT))
    signature = collect_signature()
    # Recieving 
    rec_thread = threading.Thread(target=rec_data, args=(sock,))
    rec_thread.start()
    # Sending
    send_data(sock,signature)
    sock.close()
    

if __name__ == '__main__':
    start()
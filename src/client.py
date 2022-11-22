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

import threading
import socket
import select
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


# def rec_file(sock):
#     filename = sock.recv(1024)
#     f = open(filename.decode('utf-8'), 'w')
#     data = sock.recv(1024)
#     while data:
#         f.write(data.decode('utf-8'))
#         data = sock.recv(1024)
#     f.close()


def send_data(sock):
    print(signature, end = '')
    message = input()
    sock.sendall(bytes(signature+message,'utf-8'))
    
def rec_data(sock):
    while True:
        rlist, wlist, xlist = select.select([sock],[sock],[])
        for sock in rlist:
            data = sock.recv(1024)
            if not data:
                raise Exception("We have a problem w client recv")
            print(data.decode('utf-8'))



if __name__ == '__main__':

    sock = make_socket()
    sock.connect((HOST, PORT))
    signature = collect_signature()


    rec_thread = threading.Thread(target=rec_data, args=(sock,))
    rec_thread.start()

    while True:

        # Sending 
        send_data(sock)
        
        # Receiving 
        # rec_data(sock)
        
    sock.close()
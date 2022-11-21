###################################################################################################
## Server for 1-1 messaging application with client
## Supports file transfers following a specific format
## Code largely taken from https://realpython.com/python-sockets/
###################################################################################################
## python3 server.py
## OR
## python3 server.py 127.0.0.1 4000
## where 127.0.0.1 can be any IP and 4000 can be any port 
###################################################################################################

import socket
import sys

# Server IP and port are arbitrary. Localhost used for convenience
DEFAULT_HOST = "127.0.0.1" 
DEFAULT_PORT = 65432  


def make_socket(host,port):
    """ Constructing our socket object and binding it to the given port on the given host
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()
    return s


def get_sock_from_args():
    """ Searches for comand line arguments and returns a socket with the corresponding parameters
    """
    if len(sys.argv) == 3:
        sock = make_socket(sys.argv[1],sys.argv[2])
    else:
        sock = make_socket(DEFAULT_HOST,DEFAULT_PORT)
    return sock


def collect_signature():
    """ Welcome prompt when the server first establishes a connection. 
    
    Gets the user's name and creates a signature so the client knows who's talking 

    """
    print("\nWelcome to the chatroom!")
    print("Please enter your name: ", end = '')
    name = input()
    signature = name + ": "
    return signature 

def sendfile():
    print("Enter absolute path to the file: ", end='')
    path = input()
    file = open(path, 'r')
    data = file.read() 


if __name__ == '__main__':

    sock = get_sock_from_args()
    conn, addr = sock.accept()
    signature = collect_signature()

    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(data.decode('utf-8'))
        print(signature, end = '')
        message = input()

        if message == "sendfile":
            sendfile()
        else: 
            conn.sendall(bytes(signature+message,'utf-8'))
    

    sock.close()
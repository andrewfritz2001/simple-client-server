###################################################################################################
## Receive client for 1-1 messaging application with server
###################################################################################################
## USAGE
# to be used in conjuction with send_file.py 
# import the script and call start(x) where x is the relative path to a file
###################################################################################################

import socket

# Server IP and port are arbitrary. Localhost used for convenience
HOST = "127.0.0.2" 
PORT = 12345

def make_socket():
    """ Constructing and returning a socket to connect to the server
    """
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
def rec_file(sock):
    """ First looks for the name of the file, then reads all the file contents
    """
    filename = sock.recv(1024)
    f = open(filename.decode('utf-8'), 'w')
    data = sock.recv(1024)
    while data:
        f.write(data.decode('utf-8'))
        data = sock.recv(1024)
    f.close()

def start():
    """ Opens a socket and expects to recieve a file
    """
    sock = make_socket()
    sock.connect((HOST, PORT))
    rec_file(sock)        
    sock.close()
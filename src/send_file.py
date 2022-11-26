###################################################################################################
## Send server for 1-1 messaging application with client
###################################################################################################
## USAGE
# to be used in conjuction with recv_file.py 
# import the script and call start(x) where x is the relative path to a file
###################################################################################################

import socket

# Server IP and port are arbitrary. Localhost used for convenience
DEFAULT_HOST = "127.0.0.2" 
DEFAULT_PORT = 12345


def make_socket(host,port):
    """ Constructing our socket object and binding it to the given port on the given host
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen()
    return sock

def send_file(conn, path):
    """ Parses the path and sends the file name followed by all of the data inside of the file
    """
    filename = path.split('/')
    conn.sendall(bytes(filename[-1],'utf-8'))
    f = open(path, 'r')
    data = f.read(1024) 
    while data:
        conn.send(bytes(data,'utf-8'),1024)
        data = f.read(1024)
    f.close()

def start(file_path):
    """ Takes a file path and opens a socket to send the file
    """
    sock = make_socket(DEFAULT_HOST,DEFAULT_PORT)
    conn, addr = sock.accept()
    send_file(conn,file_path)
    sock.close()    
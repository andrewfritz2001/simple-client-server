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

# def send_file(conn):
#     conn.sendall(b"sendfile") # sending notification that we're sending a file 
#     print("Enter relative path to the file: ", end='')
#     path = input()
#     filename = path.split('/')
#     conn.sendall(bytes(filename[-1],'utf-8'))

#     f = open(path, 'r')
#     data = f.read(1024) 
#     print(data)
#     while data:
#         conn.send(bytes(data,'utf-8'),1024)
#         data = f.read(1024)
#     conn.send(b"")
#     f.close()



if __name__ == '__main__':

    sock = get_sock_from_args()
    conn, addr = sock.accept()
    signature = collect_signature()

    while True:
        
        # Receiving 
        data = conn.recv(1024)
        if not data:
            break
        print(data.decode('utf-8'))

        # Sending 
        print(signature, end = '')
        message = input()
        conn.sendall(bytes(signature+message,'utf-8'))

    sock.close()
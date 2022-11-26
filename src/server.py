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

import send_file
import recv_file
import threading 
import socket
import select
import time
import sys

# Server IP and port are arbitrary. Localhost used for convenience
DEFAULT_HOST = "127.0.0.1" 
DEFAULT_PORT = 65432  

def make_socket(host,port):
    """ Constructing our socket object and binding it to the given port on the given host
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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

def file_rec():
    print("recieving file...")
    time.sleep(0.1)
    recv_file.start()
    print("file receieved!")


def file_send(conn,path):
    print('sending file...')
    conn.sendall(bytes("[]","utf-8"))
    send_file.start(path)
    print('file sent!')
    

def rec_data(conn):
    """ Function to be targeted by async thread to always listen for incoming messages 
    """
    while True:
        rlist, wlist, xlist = select.select([conn],[conn],[])
        for conn in rlist:
            data = conn.recv(1024)
            if not data:
                raise Exception("We have a problem w server recv")
            if data ==b"[]":
                file_rec()
            else:
                print(data.decode('utf-8'))

def message_sends_file(message):
    """ Returns true if a mesage is encased in closed brackets
    """
    return True if message[0] == '[' and message[-1] == ']' else False

def send_data(conn,signature):
    """ Function to be targeted by main thread and send data
    """
    while True:
        message = input()
        if message_sends_file(message):
            path = message[1:-1]
            file_send(conn,path)
        else:
            conn.sendall(bytes(signature+message,'utf-8'))

def start():
    """ Function to asynchronously send and recieve messages
    """
    sock = get_sock_from_args()
    conn, addr = sock.accept()
    signature = collect_signature()
    # Recieving 
    rec_thread = threading.Thread(target=rec_data, args=(conn,))
    rec_thread.start()
    # Sending
    send_data(conn,signature)
    sock.close()    


if __name__ == '__main__':
    start()
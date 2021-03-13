import socket
import random
from threading import Thread
host = "192.168.1.9"
port = 9876
clientSocket = socket.socket()
print(f"Connecting to {host}:{port}...")
# connect to the server
clientSocket.connect((host, port))
print("Success!")
# prompt the client for a name
name = input("Enter username: ")
name = name + ": "
print("Enter message (quit() to exit): ")
def recvMsg():
    while True:
        message = clientSocket.recv(1024).decode('utf-8')
        print("\n" + message)
recvThread = Thread(target=recvMsg) # thread for recieving messages
recvThread.daemon = True
recvThread.start()
while True:
    msgSend =  input() # need input to send next message to server
    if msgSend == 'quit()':
        break
    clientSocket.send(name.encode('utf-8') + msgSend.encode('utf-8'))
clientSocket.close() # close client socket
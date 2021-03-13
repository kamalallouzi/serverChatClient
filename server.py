import socket
import select
from threading import Thread
continueMessage = False
port = 9876
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Will make the port reusable for multiple clients even on same machine
serverSocket.bind((socket.gethostname(), port)) # Grabs the host name of server
serverSocket.listen(2) # Change value for number of clients (2 for default)
clientSockets = set() # Initializes with class to store future connections
def sendMsg(clientSocket):
    while True:
        try:
            message = clientSocket.recv(2048) # 2048 bytes max to not overload server
        except Exception: # catch if client is not connected anymore
            clientSockets.remove(clientSocket)
        except: # ignore any other errors and keep server running
            continue
        for client in clientSockets: # send to all clients to have a log of all messages for all users on screen
            client.send(message)
while True:
    clientSocket, ipAddr = serverSocket.accept() # store ip and socket of client
    print(f" {ipAddr} has connected!")
    clientSockets.add(clientSocket) # add new client to list of clients
    clientThread = Thread(target=sendMsg, args=(clientSocket,)).start() # need more than 1 thread to chat without limitations and waiting for turns
serverSocket.close() # close client at end
import socket
from src.Message import *

BUFFERSIZE = 1024
class Orchestrator:
    members = []
    serverSocket = None

    def __init__(self, host, port):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serverSocket.bind((host, port))

        self.initListening()
    
    def initListening(self):
        print('orchestrator will start listening...', flush=True)
        while True:
            response, address = self.serverSocket.recvfrom(1024)
            message = Message.parse(response)
            if(message.type == MessageType.JOIN_SWARM):
                print('join', flush=True)
                continue

            raise NotImplementedError(message.type)
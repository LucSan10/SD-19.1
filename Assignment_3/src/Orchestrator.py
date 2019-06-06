import socket
from src.Message import *

BUFFERSIZE = 1024
class Orchestrator:
    members = []
    socket = None

    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((host, port))

        self.initListening()
    
    def initListening(self):
        print('orchestrator will start listening...', flush=True)
        while True:
            response, address = self.socket.recvfrom(1024)
            message = Message.parse(response)
            if(message.type == MessageType.JOIN_SWARM):
                print('New member (%s, %s) joining swarm' % (address[0], address[1]) , flush=True)
                continue

            raise NotImplementedError(message.type)
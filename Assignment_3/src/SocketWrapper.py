from src.Message import Message
from src.Message import MessageType
import socket
import json

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 0 # PORT 0 will make the system automatically assign a port to it
BUFFERSIZE = 1024

class SocketWrapper ():
    socket = None
    sharedData = None

    def __init__(self, sharedData):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((HOST, PORT))
        self.sharedData = sharedData

    def send(self, messageType, address):
        return self.socket.sendto(
            Message(messageType).toByteStr(),
            address
        )

    def receive(self):
        response, address = self.socket.recvfrom(BUFFERSIZE)
        message = Message.parse(response)
        if(self.sharedData['failProcess']):
            if(message.type != MessageType.LEADER):
                return self.receive()

        return (response, address)
    
    def getsockname(self):
        return self.socket.getsockname()

    def close(self):
        self.socket.close()

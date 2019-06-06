import time
import socket
from src.Message import Message
from src.Message import MessageType

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 0 # PORT 0 will make the system automatically assign a port to it
BUFFERSIZE = 1024
class Member:
    orchestratorAddress = None
    clientSocket = None

    def __init__(self, orchestratorAddress):
        self.orchestratorAddress = orchestratorAddress
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def joinSwarm(self):
        message = Message(MessageType.JOIN_SWARM, 'asdas', 'a', '2')
        print(message.toByteStr(), flush=True)
        self.clientSocket.sendto(message.toByteStr(), self.orchestratorAddress)

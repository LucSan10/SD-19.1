import time
import socket
from src.Message import Message
from src.Message import MessageType
import json

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 0 # PORT 0 will make the system automatically assign a port to it
BUFFERSIZE = 1024
class Member:
    orchestratorAddress = None
    socket = None
    swarmMembers = []

    def __init__(self, orchestratorAddress):
        self.orchestratorAddress = orchestratorAddress
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((HOST, 0))
    
    def joinSwarm(self):
        message = Message(MessageType.JOIN_SWARM)
        print(message.toByteStr(), flush=True)
        self.socket.sendto(message.toByteStr(), self.orchestratorAddress)
        response, address = self.socket.recvfrom(1024)
        print("Swarm members: %s" % (response), flush=True)
        self.swarmMembers = json.loads(response)
        self.connectWithOtherMembers()
    
    def connectWithOtherMembers(self):
        for member in self.swarmMembers:
            print(member)

import threading
import sys
from enum import Enum
from src.Message import Message
from src.Message import MessageType
import json

class MemberCommunicationThread (threading.Thread):
    socket = None
    address = None
    swarmMembers = []
    orchestratorAddress = None

    def __init__(self, socket, orchestratorAddress):
        threading.Thread.__init__(self)
        self.socket = socket
        self.orchestratorAddress = orchestratorAddress
    
    def run(self):
        address = self.socket.getsockname()
        print('Starting communication (%s, %s) ' % (address[0], address[1]) , flush=True)
        self.joinSwarm()
    
    def joinSwarm(self):
        self.getSwarmMembers()

    def getSwarmMembers(self):
        message = Message(MessageType.GET_MEMBERS)
        print(message.toByteStr(), flush=True)
        self.socket.sendto(message.toByteStr(), self.orchestratorAddress)
        response, address = self.socket.recvfrom(1024)
        print("Swarm members: %s" % (response), flush=True)
        self.swarmMembers = json.loads(response)
    

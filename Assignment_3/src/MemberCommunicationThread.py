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
        self.listen()
    
    def joinSwarm(self):
        self.getSwarmMembers()
        self.enterSwarm()

    def getSwarmMembers(self):
        message = Message(MessageType.GET_MEMBERS)
        self.socket.sendto(message.toByteStr(), self.orchestratorAddress)
        response, address = self.socket.recvfrom(1024)
        self.swarmMembers = json.loads(response)
    
    def enterSwarm(self):
        message = Message(MessageType.JOIN_SWARM)
        self.socket.sendto(message.toByteStr(), self.orchestratorAddress)

        for member in self.swarmMembers:
            print(tuple(member), flush=True)
            self.socket.sendto(message.toByteStr(), tuple(member))
    
    def listen(self):
        while True:
            print('listening to receive message', flush=True)
            response, address = self.socket.recvfrom(1024)
            message = Message.parse(response)
            if(message.type == MessageType.JOIN_SWARM):
                self.saveNewMemberToSwarm(address)
                continue

            raise NotImplementedError(message.type)

    def saveNewMemberToSwarm(self, address):
        self.swarmMembers.append(address)
        print('New member (%s, %s) joining swarm' % (address[0], address[1]) , flush=True)
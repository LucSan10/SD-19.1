import threading
from enum import Enum
from src.Message import Message
from src.Message import MessageType
import json

class MemberCommunicationThread (threading.Thread):
    socket = None
    swarmMembers = []
    orchestratorAddress = None
    sharedData = None

    def __init__(self, socket, orchestratorAddress, sharedData):
        threading.Thread.__init__(self)
        self.socket = socket
        self.orchestratorAddress = orchestratorAddress
        self.sharedData = sharedData
    
    def run(self):
        address = self.socket.getsockname()
        print('Starting communication (%s, %s) ' % (address[0], address[1]) , flush=True)
        self.joinSwarm()
        self.listen()
    
    def joinSwarm(self):
        self.getSwarmMembers()
        self.enterSwarm()
        self.checkIfFirstMemberAndLeader()

    def getSwarmMembers(self):
        self.socket.send(MessageType.GET_MEMBERS, self.orchestratorAddress)
        response, address = self.socket.receive()
        message = Message.parse(response)
        self.swarmMembers = json.loads(message.params[0])
    
    def enterSwarm(self):
        self.socket.send(MessageType.JOIN_SWARM, self.orchestratorAddress)

        for member in self.swarmMembers:
            print(tuple(member), flush=True)
            self.socket.send(MessageType.JOIN_SWARM, tuple(member))
    
    def listen(self):
        while True:
            print('listening to receive message', flush=True)
            response, address = self.socket.receive()
            message = Message.parse(response)
            if(message.type == MessageType.JOIN_SWARM):
                self.saveNewMemberToSwarm(address)
                if(self.sharedData['leader']['isSelf']):
                    self.announcesLeadership(address)
                continue
            if(message.type == MessageType.LEADER):
                self.sharedData['leader']['isSelf'] = False
                self.sharedData['leader']['address'] = address
                print('Leader is ', address)
                continue
            if(message.type == MessageType.ALIVE):
                self.socket.send(MessageType.ALIVE_OK, address)
                continue
            if(message.type == MessageType.ALIVE_OK):
                self.sharedData['leader']['isAlive'] = True
                continue

            raise NotImplementedError(message.type)

    def saveNewMemberToSwarm(self, address):
        self.swarmMembers.append(address)
        print('New member (%s, %s) joining swarm' % (address[0], address[1]) , flush=True)
    
    # if is first member, declares itself as leader
    def checkIfFirstMemberAndLeader(self):
        if(len(self.swarmMembers) == 0):
            self.sharedData['leader']['isSelf'] = True
            print('is leader')

    def announcesLeadership(self, address):
        self.socket.send(MessageType.LEADER, address)

import threading
from enum import Enum
import os
from src.Message import Message
from src.Message import MessageType
import json
import time

SECONDS_TO_WAIT_FOR_ALIVE_RESPONSE = 2
SECONDS_TO_WAIT_FOR_OK_RESPONSES = 2

class CommunicationThread (threading.Thread):
    socket = None
    orchestratorAddress = None
    sharedData = None
    swarmMembers = []
    isSelfLeaderElected = None # used to check if any member answered OK on election

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
            if(message.type == MessageType.ELECTION):
                self.handleElectionMessage(message, address)
                continue
            if(message.type == MessageType.OK):
                print('Received OK', flush=True)
                self.isSelfLeaderElected = False
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

    def checkIfLeaderIsAlive(self):
        print("Checking leader status...")
        if(self.sharedData['leader']['isSelf']):
            print("I'm the leader! I am alive!", flush=True)
            return 1

        self.sharedData['leader']['isAlive'] = False
        
        self.socket.send(
            MessageType.ALIVE,
            self.sharedData['leader']['address']
        )

        time.sleep(SECONDS_TO_WAIT_FOR_ALIVE_RESPONSE)

        if(self.sharedData['leader']['isAlive'] == True):
            print("Leader is alive!", flush=True)
            return True
        else:
            print("Leader is DEAD!", flush=True)
            return False

    def startElection(self):
        self.isSelfLeaderElected = True
        print("Starting election...", flush=True)
        for member in self.swarmMembers:
            message = Message(
                MessageType.ELECTION,
                str(self.sharedData['id'])
            )
            self.socket.sendMessage(
                message.toByteStr(),
                tuple(member),
            )
        
        time.sleep(SECONDS_TO_WAIT_FOR_OK_RESPONSES)
        if(self.isSelfLeaderElected):
            print("I'm the new leader!", flush=True)
        else:
            print("I'm NOT the new leader!", flush=True)

    def handleElectionMessage(self, message, address):
        print('ELECTION', flush=True)
        processId = message.params[0]
        print(processId)
        print(type(processId))
        print(self.sharedData['id'])
        print(type(self.sharedData['id']))
        if(int(processId) < self.sharedData['id']):
            print('START ELECTION', flush=True)
            self.socket.sendMessage(
                MessageType.OK,
                address,
            )
            self.startElection()
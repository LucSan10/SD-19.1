import threading
from enum import Enum
import os
from src.Message import Message
from src.Message import MessageType
import json
import time
from src.ElectionThread import ElectionThread

SECONDS_TO_WAIT_FOR_ALIVE_RESPONSE = 2
SECONDS_TO_WAIT_FOR_OK_RESPONSES = 2

class CommunicationThread (threading.Thread):
    socket = None
    trackerAddress = None
    sharedData = None

    def __init__(self, socket, trackerAddress, sharedData):
        threading.Thread.__init__(self)
        self.socket = socket
        self.trackerAddress = trackerAddress
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
        self.socket.send(MessageType.GET_MEMBERS, self.trackerAddress)
        response, address = self.socket.receive()
        message = Message.parse(response)
        self.sharedData['swarmMembers'] = json.loads(message.params[0])
    
    def enterSwarm(self):
        self.socket.send(MessageType.JOIN_SWARM, self.trackerAddress)

        for member in self.sharedData['swarmMembers']:
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
                    self.announceLeadership(address)
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
                print('Received OK for election id ', message.params[1], flush=True)
                self.sharedData['elections'][message.params[1]]['isLeader'] = False
                continue

            raise NotImplementedError(message.type)

    def saveNewMemberToSwarm(self, address):
        self.sharedData['swarmMembers'].append(address)
        print('New member (%s, %s) joining swarm' % (address[0], address[1]) , flush=True)
    
    # if is first member, declares itself as leader
    def checkIfFirstMemberAndLeader(self):
        if(len(self.sharedData['swarmMembers']) == 0):
            self.sharedData['leader']['isSelf'] = True
            print('is leader')

    def announceLeadership(self, address):
        self.socket.send(MessageType.LEADER, address)


    def checkIfLeaderIsAlive(self):
        print("Checking leader status...")
        if(self.sharedData['leader']['isSelf']):
            print("I'm the leader! I am alive!", flush=True)
            return

        self.sharedData['leader']['isAlive'] = False
        
        self.socket.send(
            MessageType.ALIVE,
            self.sharedData['leader']['address']
        )

        time.sleep(SECONDS_TO_WAIT_FOR_ALIVE_RESPONSE)

        if(self.sharedData['leader']['isAlive'] == True):
            print("Leader is alive!", flush=True)
            return
        else:
            print("Leader is DEAD!", flush=True)
            self.startElection()

    def handleElectionMessage(self, message, address):
        processId = message.params[0]
        if(int(processId) < self.sharedData['id']):
            print('sending OK for election ID ', message.params[1], flush=True)
            message = Message(
                MessageType.OK,
                str(self.sharedData['id']),
                message.params[1]
            )
            self.socket.sendMessage(
                message.toByteStr(),
                address,
            )
            self.startElection()
    
    def startElection(self):
        electionThread = ElectionThread(self.socket, self.sharedData)
        electionThread.start()
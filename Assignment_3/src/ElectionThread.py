import threading
from enum import Enum
import os
from src.Message import Message
from src.Message import MessageType
import json
import time

SECONDS_TO_WAIT_FOR_OK_RESPONSES = 2

class ElectionThread (threading.Thread):
    socket = None
    sharedData = None

    def __init__(self, socket, sharedData):
        threading.Thread.__init__(self)
        self.socket = socket
        self.sharedData = sharedData
    
    def run(self):
        self.startElection()
    
    def startElection(self):
        print("Starting election...", flush=True)
        electionId = str(threading.get_ident())
        print('ELECTION STARTED WITH ID ', electionId)
        self.sharedData['elections'][electionId] = {
            "isLeader": True
        }

        for member in self.sharedData['swarmMembers']:
            message = Message(
                MessageType.ELECTION,
                str(self.sharedData['id']),
                electionId
            )
            self.socket.sendMessage(
                message.toByteStr(),
                tuple(member),
            )
        
        time.sleep(SECONDS_TO_WAIT_FOR_OK_RESPONSES)

        if(self.sharedData['elections'][electionId]['isLeader']):
            print("I'm the new leader!", flush=True)
            self.sharedData['leader']['isSelf'] = True
            self.broadcastLeadership()
        else:
            print("I'm NOT the new leader!", flush=True)
    
    def broadcastLeadership(self):
        for member in self.sharedData['swarmMembers']:
            print("broadcasting leadership to (%s, %s)" % (member[0], member[1]), flush=True)
            self.socket.send(MessageType.LEADER, tuple(member))

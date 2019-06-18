import threading
from enum import Enum
import os
from src.Message import Message
from src.Message import MessageType
import json
import time
from src.utils import log

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
        log("Starting election...")
        electionId = str(threading.get_ident())
        log('ELECTION STARTED WITH ID ', electionId)
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
            log("I'm the new leader!")
            self.sharedData['leader']['isSelf'] = True
            self.broadcastLeadership()
        else:
            log("I'm NOT the new leader!")
    
    def broadcastLeadership(self):
        for member in self.sharedData['swarmMembers']:
            log("broadcasting leadership to (%s, %s)" % (member[0], member[1]))
            self.socket.send(MessageType.LEADER, tuple(member))

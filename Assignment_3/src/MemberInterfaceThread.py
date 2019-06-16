import threading
import sys
from enum import Enum
from src.Message import Message
from src.Message import MessageType
import json
import time

SECONDS_TO_WAIT_FOR_ALIVE_RESPONSE = 2

class MemberInterfaceThread (threading.Thread):
    OPTIONS = [
        {
            "value": "1",
            "description": "finish process",
            "handler": "finishProcess"
        },
        {
            "value": "2",
            "description": "check whether leader is alive",
            "handler": "isLeaderIsAlive"
        }
    ]

    socket = None
    sharedData = None

    def __init__(self, socket, sharedData):
        threading.Thread.__init__(self)
        self.socket = socket
        self.sharedData = sharedData
    
    def run(self):
        address = self.socket.getsockname()
        print('Starting interface (%s, %s) ' % (address[0], address[1]) , flush=True)
        while True:
            self.printMainMenu()
            option = input('Choose an option: ')
            self.handleOption(option)
    
    def printMainMenu(self):
        print('==========================')
        print('Options:')
        for option in self.OPTIONS:
            print(option["value"], ' - ', option['description'])

    def handleOption(self, choice):
        for option in self.OPTIONS:
            if(option["value"] == choice):
                getattr(self, option['handler'])()
    
    def finishProcess(self):
        print('finishing', flush=True)
        self.socket.close()
        sys.exit(1)

    def isLeaderIsAlive(self):
        if(self.sharedData['leader']['isSelf']):
            print("I'm the leader! I am alive!", flush=True)
            return

        self.sharedData['leader']['isAlive'] = False
        
        self.socket.sendto(
            Message(MessageType.ALIVE).toByteStr(),
            self.sharedData['leader']['address']
        )

        time.sleep(SECONDS_TO_WAIT_FOR_ALIVE_RESPONSE)

        if(self.sharedData['leader']['isAlive'] == True):
            print("Leader is alive!", flush=True)
        else:
            print("Leader is DEAD!", flush=True)

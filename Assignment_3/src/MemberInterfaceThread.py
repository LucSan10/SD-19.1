import threading
import sys
from enum import Enum
from src.Message import Message
from src.Message import MessageType
import json
import time

SECONDS_TO_WAIT_FOR_ALIVE_RESPONSE = 2

class OPTIONS(Enum):
    FINISH = "1"
    CHECK_LEADER_ALIVE = "2"
    ELECTION = "3"


class MemberInterfaceThread (threading.Thread):
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
        print(OPTIONS.FINISH.value + ' - finish process')
        print(OPTIONS.CHECK_LEADER_ALIVE.value + ' - check whether leader is alive')

    def handleOption(self, option):
        if(option == OPTIONS.FINISH.value):
            print('finishing', flush=True)
            self.socket.close()
            sys.exit(1)
        if(option == OPTIONS.CHECK_LEADER_ALIVE.value):
            self.isLeaderIsAlive()

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

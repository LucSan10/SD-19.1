import threading
from enum import Enum
from src.Message import Message
from src.Message import MessageType
import time
import json

SECONDS_TO_WAIT_FOR_ALIVE_RESPONSE = 2

class LeaderCheckingThread (threading.Thread):
    socket = None
    sharedData = None

    def __init__(self, socket, sharedData):
        threading.Thread.__init__(self)
        self.socket = socket
        self.sharedData = sharedData

    def run(self):
        address = self.socket.getsockname()
        print('Starting checker (%s, %s) ' % (address[0], address[1]) , flush=True)
        while True:
            time.sleep(5)
            self.checkIfLeaderIsAlive()        

    def checkIfLeaderIsAlive(self):
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
        else:
            print("Leader is DEAD!", flush=True)
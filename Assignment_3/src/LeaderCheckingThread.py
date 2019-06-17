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
    communicationThread = None

    def __init__(self, socket, sharedData, communicationThread):
        threading.Thread.__init__(self)
        self.socket = socket
        self.sharedData = sharedData
        self.communicationThread = communicationThread

    def run(self):
        address = self.socket.getsockname()
        print('Starting checker (%s, %s) ' % (address[0], address[1]) , flush=True)
        while True:
            time.sleep(5)
            self.communicationThread.checkIfLeaderIsAlive()

import threading
import os
from enum import Enum
from src.Message import Message
from src.Message import MessageType
import json
import time
from src.functions import checkIfLeaderIsAlive 

SECONDS_TO_WAIT_FOR_ALIVE_RESPONSE = 2

class InterfaceThread (threading.Thread):
    OPTIONS = [
        {
            "value": "1",
            "description": "finish process",
            "handler": "finishProcess"
        },
        {
            "value": "2",
            "description": "check whether leader is alive",
            "handler": "checkIfLeaderIsAlive"
        },
        {
            "value": "3",
            "description": "fail process",
            "handler": "failProcess"
        },
        {
            "value": "4",
            "description": "recover process",
            "handler": "recoverProcess"
        }
    ]

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
                return getattr(self, option['handler'])()
        print('Option not recognized!', flush=True)
    
    def finishProcess(self):
        print('finishing', flush=True)
        self.socket.close()
        os._exit(0)

    def checkIfLeaderIsAlive(self):
        self.communicationThread.checkIfLeaderIsAlive()

    def failProcess(self):
        self.sharedData['failProcess'] = True

    def recoverProcess(self):
        self.sharedData['failProcess'] = False

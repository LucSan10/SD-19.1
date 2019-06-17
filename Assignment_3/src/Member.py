import time
from src.InterfaceThread import InterfaceThread
from src.CommunicationThread import CommunicationThread
from src.SocketWrapper import SocketWrapper
import threading

class Member:
    interfaceThread = None
    communcationThread = None

    def __init__(self, orchestratorAddress):
        sharedData = {
            "leader": {
                "isSelf": False, # is this member the leader
                "address": None, # if isLeader false, stores the leader address
                "isAlive": False, # whether the leader is alive or not
            },
            "failProcess": False # whether the communication of the process blocked "failed member"
        }

        socket = SocketWrapper(sharedData)

        self.interfaceThread = InterfaceThread(socket, sharedData)
        self.communicationThread = CommunicationThread(socket, orchestratorAddress, sharedData)

    def start(self):
        self.interfaceThread.start()
        self.communicationThread.start()

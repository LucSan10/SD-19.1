import time
import os
from src.LeaderCheckingThread import LeaderCheckingThread
from src.InterfaceThread import InterfaceThread
from src.CommunicationThread import CommunicationThread
from src.SocketWrapper import SocketWrapper
import threading

class Member:
    interfaceThread = None
    communcationThread = None
    leaderCheckingThread = None

    def __init__(self, orchestratorAddress):
        id = os.getpid()
        print('Process ID: ', id, flush=True)
        sharedData = {
            "leader": {
                "isSelf": False, # is this member the leader
                "address": None, # if isLeader false, stores the leader address
                "isAlive": False, # whether the leader is alive or not
            },
            "id": id, # process id
            "failProcess": False # whether the communication of the process blocked "failed member"
        }

        socket = SocketWrapper(sharedData)

        self.communicationThread = CommunicationThread(socket, orchestratorAddress, sharedData)
        self.interfaceThread = InterfaceThread(socket, sharedData, self.communicationThread)
        self.leaderCheckingThread = LeaderCheckingThread(socket, sharedData, self.communicationThread)

    def start(self):
        self.interfaceThread.start()
        self.leaderCheckingThread.start()
        self.communicationThread.start()
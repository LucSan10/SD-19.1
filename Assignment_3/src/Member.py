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
        sharedData = {
            "leader": {
                "isSelf": False, # is this member the leader
                "address": None, # if isLeader false, stores the leader address
                "isAlive": False, # whether the leader is alive or not
            },
            "id": os.getpid(), # process id
            "failProcess": False, # whether the communication of the process blocked "failed member"
            "swarmMembers": []
        }

        socket = SocketWrapper(sharedData)

        self.interfaceThread = InterfaceThread(socket, sharedData)
        self.communicationThread = CommunicationThread(socket, orchestratorAddress, sharedData)
        self.leaderCheckingThread = LeaderCheckingThread(socket, sharedData)

    def start(self):
        self.interfaceThread.start()
        self.leaderCheckingThread.start()
        self.communicationThread.start()
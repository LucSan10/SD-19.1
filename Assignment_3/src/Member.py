import time
from src.MemberInterfaceThread import MemberInterfaceThread
from src.MemberCommunicationThread import MemberCommunicationThread
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

        self.interfaceThread = MemberInterfaceThread(socket, sharedData)
        self.communicationThread = MemberCommunicationThread(socket, orchestratorAddress, sharedData)

    def start(self):
        self.interfaceThread.start()
        self.communicationThread.start()

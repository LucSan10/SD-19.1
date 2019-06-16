import time
import socket
from src.MemberInterfaceThread import MemberInterfaceThread
from src.MemberCommunicationThread import MemberCommunicationThread

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 0 # PORT 0 will make the system automatically assign a port to it
BUFFERSIZE = 1024
class Member:
    socket = None
    interfaceThread = None
    communcationThread = None

    def __init__(self, orchestratorAddress):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((HOST, 0))
        sharedData = {
            "leader": {
                "isSelf": False, # is this member the leader
                "address": None # if isLeader false, stores the leader address
            }
        }

        self.interfaceThread = MemberInterfaceThread(self.socket, sharedData)
        self.communicationThread = MemberCommunicationThread(self.socket, orchestratorAddress, sharedData)
    
    def start(self):
        self.interfaceThread.start()
        self.communicationThread.start()

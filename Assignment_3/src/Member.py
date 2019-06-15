import time
import socket
from src.Message import Message
from src.Message import MessageType
from src.MemberInterfaceThread import MemberInterfaceThread
import json

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 0 # PORT 0 will make the system automatically assign a port to it
BUFFERSIZE = 1024
class Member:
    orchestratorAddress = None
    socket = None
    swarmMembers = []
    interfaceThread = None

    def __init__(self, orchestratorAddress):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((HOST, 0))
        self.interfaceThread = MemberInterfaceThread(self.socket)
    
    def start(self):
        self.interfaceThread.start()

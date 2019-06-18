from src.Message import Message
from src.Message import MessageType
import socket
import json
from src.utils import log

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 0 # PORT 0 will make the system automatically assign a port to it
BUFFERSIZE = 1024

class SocketWrapper ():
    socket = None
    sharedData = None
    statistics = {
        "sent" : {
            "OK": 0,
            "ELECTION": 0,
            "LEADER": 0,
            "ALIVE": 0,
            "ALIVE_OK": 0,
            "JOIN_SWARM": 0,
            "GET_MEMBERS": 0,
            "KILL": 0
        },
        "received" : {
            "OK": 0,
            "ELECTION": 0,
            "LEADER": 0,
            "ALIVE": 0,
            "ALIVE_OK": 0,
            "JOIN_SWARM": 0,
            "GET_MEMBERS": 0,
            "KILL": 0
        }
    }

    def __init__(self, sharedData):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((HOST, PORT))
        self.sharedData = sharedData

    def send(self, messageType, address):
        return self.sendMessage(
            Message(messageType).toByteStr(),
            address
        )
    
    def sendMessage(self, message, address):
        messageParsed = Message.parse(message)
        name = messageParsed.type.name
        if (self.sharedData['failProcess']):
            log("%s message sent blocked" % name)
            return

        log("%s message sent" % name)

        self.storeStatistics(messageParsed.type, 'sent')

        return self.socket.sendto(
            message,
            address
        )

    def receive(self):
        response, address = self.socket.recvfrom(BUFFERSIZE)
        message = Message.parse(response)
        if(self.sharedData['failProcess']):
            if(message.type != MessageType.LEADER):
                log('%s message received ignored' % message.type.name)
                return self.receive()

        self.storeStatistics(message.type, 'received')

        log('%s message received' % message.type.name)
        return (response, address)
    
    def storeStatistics(self, messageType, direction):
        with self.sharedData['statisticsLock']:
            self.statistics[direction][messageType.name] += 1
    
    def getsockname(self):
        return self.socket.getsockname()

    def close(self):
        self.socket.close()

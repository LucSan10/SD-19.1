import sys
import socket
from src.Message import Message
from src.Message import MessageType
import json

ORCHESTRATOR_ADDRESS = ("127.0.0.1", 2000)
HOST = '127.0.0.1'

def main():
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mySocket.bind((HOST, 0))
    finishProcess(ORCHESTRATOR_ADDRESS, mySocket)

def finishProcess(address, mySocket):
    print(address, flush=True)
    message = Message(MessageType.KILL)
    mySocket.sendto(message.toByteStr(), address)

main()
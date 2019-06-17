import threading
import time
from enum import Enum
from src.Message import Message
from src.Message import MessageType
import json

SECONDS_TO_WAIT_FOR_ALIVE_RESPONSE = 2

def checkIfLeaderIsAlive(instance):
    print("Checking leader status...")
    if(instance.sharedData['leader']['isSelf']):
        print("I'm the leader! I am alive!", flush=True)
        return

    instance.sharedData['leader']['isAlive'] = False
    
    instance.socket.send(
        MessageType.ALIVE,
        instance.sharedData['leader']['address']
    )

    time.sleep(SECONDS_TO_WAIT_FOR_ALIVE_RESPONSE)

    if(instance.sharedData['leader']['isAlive'] == True):
        print("Leader is alive!", flush=True)
    else:
        print("Leader is DEAD!", flush=True)

# def startElection(instance):
#     for ()
#     self.socket.send(MessageType.LEADER, address)
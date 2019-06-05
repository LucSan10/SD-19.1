from enum import Enum

class MessageType(Enum):
    OK = 1
    ELECTION = 2
    LEADER = 3
    ALIVE = 4
    ALIVE_OK = 5

class Message:
    type = None
    params = None

    def __init__(self, type, *params):
        self.type = type
        self.params = params

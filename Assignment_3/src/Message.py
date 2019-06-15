from enum import Enum

class MessageType(Enum):
    OK = 1
    ELECTION = 2
    LEADER = 3
    ALIVE = 4
    ALIVE_OK = 5
    JOIN_SWARM = 6
    GET_MEMBERS = 7
    KILL = 8

class Message:
    type = None
    params = None

    def __init__(self, type, *params):
        self.type = type
        self.params = params
    
    def __str__(self):
        return str(self.type.value) + '|' + '|'.join(self.params)
    
    @staticmethod
    def parse(message):
        text = message.decode('utf8').split('|')   
        return Message(
            MessageType(int(text[0])),
            *text[1:]
        )

    def toByteStr(self):
        return str.encode(self.__str__())
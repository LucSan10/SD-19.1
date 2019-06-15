import threading
import sys
from enum import Enum

class OPTIONS(Enum):
    FINISH = "1"
    ELECTION = "2"

class MemberInterfaceThread (threading.Thread):
    socket = None
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket
    
    def run(self):
        address = self.socket.getsockname()
        print('Starting interface (%s, %s) ' % (address[0], address[1]) , flush=True)
        while True:
            self.printMainMenu()
            option = input('Choose an option: ')
            self.handleOption(option)
    
    def printMainMenu(self):
        print('==========================')
        print('Options:')
        print(OPTIONS.FINISH.value + ' - finish process')

    def handleOption(self, option):
        if(option == OPTIONS.FINISH.value):
            print('finishing', flush=True)
            self.socket.close()
            sys.exit(1)
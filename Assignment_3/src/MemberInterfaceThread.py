import threading

class MemberInterfaceThread (threading.Thread):
    socket = None
    address = None
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket
    def run(self):
        address = self.socket.getsockname()
        print('Starting interface (%s, %s) ' % (address[0], address[1]) , flush=True)
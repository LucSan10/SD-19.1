import socket

BUFFERSIZE = 1024
class Orchestrator:
    members = []
    serverSocket = None

    def __init__(self, host, port):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serverSocket.bind((host, port))

        self.initListening()
    
    def initListening(self):
        print('orchestrator will start listening...', flush=True)
        while True:
            message, address = self.serverSocket.recvfrom(1024)
            print("message: %s \n address: %s" % (message, address), flush=True)

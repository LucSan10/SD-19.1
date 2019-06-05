import time
import socket

BUFFERSIZE = 1024
class Orchestrator:
    port = None
    host = None
    members = []

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.initListening()
    
    def initListening(self):
        print("TODO Listening")

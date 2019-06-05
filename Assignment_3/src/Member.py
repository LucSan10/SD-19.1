import time
import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 0 # PORT 0 will make the system automatically assign a port to it
BUFFERSIZE = 1024
class Member:
    orchestratorPort = None

    def __init__(self, orchestratorPort):
        self.orchestratorPort = orchestratorPort

        print("import message")

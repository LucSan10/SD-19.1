from src.Member import *

import socket
ORCHESTRATOR_ADDRESS = ("127.0.0.1", 2000)

member = Member(ORCHESTRATOR_ADDRESS)
member.start()
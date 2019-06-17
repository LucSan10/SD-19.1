from src.Member import Member

import socket
TRACKER_ADDRESS = ("127.0.0.1", 2000)

member = Member(TRACKER_ADDRESS)
member.start()
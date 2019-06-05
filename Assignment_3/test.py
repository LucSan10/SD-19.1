from src.Member import Member
from src.Message import Message

import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = b'test'
addr = ("127.0.0.1", 2000)
client_socket.sendto(message, addr)
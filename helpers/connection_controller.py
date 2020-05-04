import socket
from constants import DEFAULT_PORT, DEFAULT_ADDR

class ConnectionController:
    host = DEFAULT_ADDR
    port = DEFAULT_PORT

    def __init__(self, host, port):
        self.host = host
        self.port = port

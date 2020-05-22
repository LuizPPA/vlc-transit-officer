import socket
from constants import DEFAULT_PORT, DEFAULT_ADDR

class ConnectionController:

    def __init__(self, host=DEFAULT_ADDR, port=DEFAULT_PORT):
        self.host = host
        self.port = port

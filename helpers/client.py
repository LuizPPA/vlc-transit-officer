import socket

from helpers.connection_controller import ConnectionController

class Client(ConnectionController):

    def connect(self):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.connect((self.host, self.port))
        return tcp

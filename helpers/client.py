import socket

from helpers.connection_controller import ConnectionController
from Player import Player
from constants import DEFAULT_ADDR

class Client(ConnectionController):

    def connect(self, host = DEFAULT_ADDR):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.connect((host, self.port))
        return tcp

    def create_player(self):
        player = Player()
        player.resize(1024, 768)
        player.setWindowTitle('Client')
        return player

import socket

from helpers.connection_controller import ConnectionController
from Player import Player

class Server(ConnectionController):
    clients = []

    def serve(self, peers = 1):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        origin = (self.host, self.port)
        tcp.bind(origin)
        tcp.listen(peers)
        for _i in range(0, peers):
            try:
                connection, client = tcp.accept()
                self.clients.append({
                    'connection': connection,
                    'client': client
                })
                print('Serving to ', client)
            except socket.timeout:
                print('Could not connect to all peers')

    def create_player(self):
        player = Player()
        player.resize(1024, 768)
        player.setWindowTitle('Host')
        player.stop_callback = lambda: self.broadcast('0')
        player.play_pause_callback = lambda: self.broadcast('1')
        player.set_position_callback = lambda: self.broadcast('2-' + player.stringify_slider_position())
        return player

    def broadcast(self, message):
        for client in self.clients:
            client['connection'].send(message.encode('utf-8'))

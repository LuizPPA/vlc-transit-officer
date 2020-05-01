import socket

def bufsize():
    return 4096

class ConnectionController:
    host = '127.0.0.1'
    port = 8080
    clients = []

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def serve(self, peers = 1):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        origin = (self.host, self.port)
        tcp.bind(origin)
        tcp.listen(peers)
        for i in range(0, peers):
            try:
                connection, client = tcp.accept()
                self.clients.append({
                    'connection': connection,
                    'client': client
                })
                print('Serving to ', client)
            except socket.timeout:
                print('Could not connect to all peers')
                return self.clients

        return self.clients

    def connect(self):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.connect((self.host, self.port))
        return tcp

    def broadcast(self, message):
        for client in self.clients:
            client['connection'].send(message.encode('utf-8'))

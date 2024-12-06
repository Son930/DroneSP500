import socket

class ConnectionManager:
    def __init__(self):
        self.sock = None

    def initialize_sockets(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def cleanup_sockets(self):
        if self.sock:
            self.sock.close()

    def create_udp_socket_and_prepare(self, ip, port):
        self.initialize_sockets()
        self.server_addr = (ip, port)
        # Optionally bind to ensure it's ready for receiving
        self.sock.bind(('0.0.0.0', port))
        print(f"UDP socket created for communication with {ip}:{port}")
        return self.sock

class CommandSender:
    def __init__(self, sock, server_addr):
        self.sock = sock
        self.server_addr = server_addr

    def convert_to_ascii(self, input_str):
        return ''.join([char if ord(char) < 128 else '?' for char in input_str])

    def send_command(self, command):
        ascii_command = self.convert_to_ascii(command)
        self.sock.sendto(ascii_command.encode('ascii'), self.server_addr)
        print(f"Command sent (ASCII): {ascii_command}")

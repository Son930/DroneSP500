import binascii

class DataReceiver:
    def __init__(self, sock):
        self.sock = sock

    def decode_and_display(self, data):
        # Display the raw data as hexadecimal
        print("Received raw data (Hex):", binascii.hexlify(data).decode())

        # Display the raw data in binary format
        print("Received raw data (Binary):", ' '.join(format(byte, '08b') for byte in data))

        # Interpret as plain text if ASCII-readable
        ascii_data = ''.join((chr(byte) if 32 <= byte <= 127 else '.') for byte in data)
        print("Interpreted as Plain Text (ASCII):", ascii_data)

    def receive_data(self):
        while True:
            try:
                data, addr = self.sock.recvfrom(2048)
                self.decode_and_display(data)
            except OSError as e:
                print(f"Socket error: {e}")
                break

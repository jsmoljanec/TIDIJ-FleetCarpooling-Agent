import socket

from .strings import Strings


class UDPServer:
    def __init__(self, device, port=50001):
        self.UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.device = device
        self.port = port
        self.setup_socket()

    def setup_socket(self):
        try:
            self.UDPServerSocket.bind((self.device, self.port))
            print(Strings.AGENT_UP.format(self.device, self.port))
            print(Strings.MESSAGE_SEPARATOR)
        except socket.error as e:
            print(Strings.ERROR_UDP_BINDING.format(e))
            raise e

    def receive_commands(self, message_handler):
        while True:
            bytes_address_pair = self.UDPServerSocket.recvfrom(1024)
            message = bytes_address_pair[0].decode("utf-8")
            address = bytes_address_pair[1]

            message_handler.process_udp_message(message, address)

    def send_udp_message(self, message, address):
        self.UDPServerSocket.sendto(message.encode("utf-8"), address)

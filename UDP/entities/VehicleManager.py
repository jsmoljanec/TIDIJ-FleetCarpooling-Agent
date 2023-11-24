import socket
import threading
import time


class VehicleManager:
    def __init__(self, start, list_of_coordinates):
        self.is_running = False
        self.stop_requested = False
        self.location = start
        self.coordinates = list_of_coordinates
        self.UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPServerSocket.bind(('localhost', 50001))
        print("UDP server up and listening")

    def start_vehicle(self, destination_address):
        self.is_running = True
        sequence_number = 1

        # while not self.stop_requested:
        #     self.UDPServerSocket.sendto(f"Location: {self.location}".encode("utf-8"), destination_address)
        #     self.location["latitude"] += 0.001
        #     self.location["longitude"] += 0.001
        #     print(f"Vehicle is driving and currently at: {self.location}")
        #
        #     sequence_number += 1
        #     time.sleep(0.5)

        for coordinate in self.coordinates:
            self.location = {
                "latitude": coordinate[0],
                "longitude": coordinate[1]
            }
            print(f"Vehicle is driving and currently at: {self.location}")
            self.UDPServerSocket.sendto(f"Location: {self.location}".encode("utf-8"), destination_address)
            sequence_number += 1
            time.sleep(0.5)

        if self.is_running:
            self.is_running = False
            self.stop_requested = False
            print("Vehicle stopped.")

    def stop_vehicle(self, destination_address):
        self.stop_requested = True
        self.UDPServerSocket.sendto("Vehicle stopped!".encode("utf-8"), destination_address)

    def receive_commands(self):
        while True:
            bytes_address_pair = self.UDPServerSocket.recvfrom(1024)
            message = bytes_address_pair[0].decode("utf-8")
            address = bytes_address_pair[1]

            command = message.lower()

            # client_ip = f"Client IP Address: {address}"
            # print(f"{message}\n{client_ip}\n-----------------\n")

            if command == "start":
                print(f"Vehicle from this address: {address} started ride.")
                vehicle_thread = threading.Thread(target=self.start_vehicle, args=(address,))
                vehicle_thread.start()
            elif command == "stop":
                print(f"Vehicle from this address: {address} stopped ride.")
                self.stop_vehicle(address)

            reply_msg = "Hello test agent, thanks for messaging!\n-----------------\n"
            self.UDPServerSocket.sendto(reply_msg.encode("utf-8"), address)

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
        self.last_stopped_location = None
        self.last_index = 0
        print("UDP server up and listening")

    def start_vehicle(self, destination_address):
        self.is_running = True
        self.stop_requested = False
        sequence_number = 1

        if self.last_stopped_location:
            self.location = self.last_stopped_location
            print(f"Resuming ride from the last stopped location: {self.location}")

        if self.stop_requested:
            self.last_stopped_location = self.location

        if self.last_index > 0:
            self.last_index -= 1

        for i in range(self.last_index, len(self.coordinates)):
            if self.stop_requested:
                self.last_stopped_location = self.location
                self.last_index = i
                break

            coordinate = self.coordinates[i]
            self.location = {
                "latitude": coordinate[0],
                "longitude": coordinate[1]
            }
            print(f"Vehicle is driving and currently at: {self.location}")
            self.UDPServerSocket.sendto(f"Location: {self.location}".encode("utf-8"), destination_address)
            sequence_number += 1
            time.sleep(0.5)

    def stop_vehicle(self, destination_address):
        self.stop_requested = True
        self.is_running = False
        self.UDPServerSocket.sendto("Vehicle stopped!".encode("utf-8"), destination_address)

    def receive_commands(self):
        while True:
            bytes_address_pair = self.UDPServerSocket.recvfrom(1024)
            message = bytes_address_pair[0].decode("utf-8")
            address = bytes_address_pair[1]

            command = message.lower()

            if command == "start":
                print(f"Vehicle from this address: {address} started ride.")
                vehicle_thread = threading.Thread(target=self.start_vehicle, args=(address,))
                vehicle_thread.start()
            elif command == "stop":
                print(f"Vehicle from this address: {address} stopped ride.")
                self.stop_vehicle(address)

            reply_msg = "Hello test agent, thanks for messaging!\n-----------------\n"
            self.UDPServerSocket.sendto(reply_msg.encode("utf-8"), address)

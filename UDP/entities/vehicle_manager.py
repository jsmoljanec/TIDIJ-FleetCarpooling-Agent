import socket
import threading
import time


class VehicleManager:
    def __init__(self, list_of_coordinates):
        self.is_running = False
        self.stop_requested = False
        self.restart_requested = False
        self.location = None
        self.coordinates = list_of_coordinates
        self.UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPServerSocket.bind(('localhost', 50001))
        self.last_stopped_location = None
        self.last_index = 0
        self.last_command = None
        print("UDP server up and listening")

    def change_vehicle_state(self, is_running, stop_requested, restart_requested):
        self.is_running = is_running
        self.stop_requested = stop_requested
        self.restart_requested = restart_requested

    def start_vehicle(self, destination_address):
        self.change_vehicle_state(True, False, False)
        sequence_number = 1

        if self.last_stopped_location:
            self.location = self.last_stopped_location
            print(f"Resuming ride from the last stopped location: {self.location}")

        if self.last_index > 0:
            self.last_index -= 1

        for i in range(self.last_index, len(self.coordinates)):
            if self.restart_requested:
                self.last_stopped_location = None
                self.last_index = 0
                break

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
        self.change_vehicle_state(False, True, False)
        self.UDPServerSocket.sendto("Vehicle stopped!".encode("utf-8"), destination_address)

    def restart_vehicle_position(self, destination_address):
        self.change_vehicle_state(False, True, True)

        coordinate = self.coordinates[0]
        self.location = {
            "latitude": coordinate[0],
            "longitude": coordinate[1]
        }

        self.last_command = "restart"
        self.UDPServerSocket.sendto(f"Location: {self.location}".encode("utf-8"), destination_address)

    def process_start_command(self, address):
        if self.is_running or self.last_command == "start":
            print("Vehicle is already running or has already received a start command. Cannot start again.")
        else:
            print(f"Vehicle from this address: {address} started ride.")
            self.last_command = "start"
            vehicle_thread = threading.Thread(target=self.start_vehicle, args=(address,))
            vehicle_thread.start()

    def process_stop_command(self, address):
        if not self.is_running or self.last_command == "stop":
            print("Vehicle is not currently running or has already received a stop command. Cannot stop.")
        else:
            print(f"Vehicle from this address: {address} stopped ride.")
            self.last_command = "stop"
            self.stop_vehicle(address)

    def process_restart_command(self, address):
        if self.last_command == "restart":
            print("Vehicle is already restarted!")
        else:
            self.last_command = "restart"
            if self.stop_requested:
                print("Restarting vehicle from the beginning...")
                self.last_stopped_location = None
                self.last_index = 0
                self.restart_vehicle_position(address)
            else:
                print("Vehicle cannot be restarted. It is not currently stopped.")

    def receive_commands(self):
        while True:
            bytes_address_pair = self.UDPServerSocket.recvfrom(1024)
            message = bytes_address_pair[0].decode("utf-8")
            address = bytes_address_pair[1]

            command = message.lower()

            if command == "start":
                self.process_start_command(address)
            elif command == "stop":
                self.process_stop_command(address)
            elif command == "restart":
                self.process_restart_command(address)

            reply_msg = "Hello test agent, thanks for messaging!\n-----------------\n"
            self.UDPServerSocket.sendto(reply_msg.encode("utf-8"), address)
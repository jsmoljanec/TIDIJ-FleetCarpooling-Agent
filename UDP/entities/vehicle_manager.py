import socket
import threading
import time
import os
from dotenv import load_dotenv

from UDP.entities.firebase_admin_manager import FirebaseAdminManager


class VehicleState:
    def __init__(self):
        self.is_running = False
        self.stop_requested = False
        self.restart_requested = False
        self.last_stopped_location = None
        self.last_index = 0
        self.last_command = None
        self.speed = 1.5


class VehicleManager:
    def __init__(self, list_of_coordinates):
        self.coordinates = list_of_coordinates
        self.location = {
            "latitude": self.coordinates[0][0],
            "longitude": self.coordinates[0][1]
        }
        self.UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPServerSocket.bind(('localhost', 50001))
        self.vehicle_states = {}  # Rječnik za praćenje stanja svakog vozila
        print("UDP server up and listening")
        print("---------------------------")

        load_dotenv()
        firebase_credentials_path = os.getenv("CREDENTIALS_PATH")
        firebase_database_url = os.getenv("DATABASE_URL")
        self.firebaseManager = FirebaseAdminManager(firebase_credentials_path, firebase_database_url)

    def get_vehicle_state(self, vehicle_id):
        if vehicle_id not in self.vehicle_states:
            self.vehicle_states[vehicle_id] = VehicleState()
        return self.vehicle_states[vehicle_id]

    def change_vehicle_state(self, vehicle_id, is_running, stop_requested, restart_requested):
        state = self.get_vehicle_state(vehicle_id)
        state.is_running = is_running
        state.stop_requested = stop_requested
        state.restart_requested = restart_requested

    def send_current_location(self, address, vehicle_id):
        self.UDPServerSocket.sendto(f"Location for vehicle {vehicle_id}: {self.location}".encode("utf-8"), address)
        print(f"Vehicle {vehicle_id} is currently at: {self.location}")

    def process_start_command(self, address, vehicle_id):
        state = self.get_vehicle_state(vehicle_id)

        if state.is_running or state.last_command == "start":
            print(
                f"Vehicle {vehicle_id} is already running or has already received a start command. Cannot start again.")
        else:
            print(f"Vehicle {vehicle_id} from this address: {address} started ride.")
            state.last_command = "start"
            vehicle_thread = threading.Thread(target=self.start_vehicle, args=(address, vehicle_id))
            vehicle_thread.start()

    def process_stop_command(self, address, vehicle_id):
        state = self.get_vehicle_state(vehicle_id)

        if not state.is_running or state.last_command == "stop":
            print(f"Vehicle {vehicle_id} is not currently running or has already received a stop command. Cannot stop.")
        else:
            print(f"Vehicle {vehicle_id} from this address: {address} stopped ride.")
            state.last_command = "stop"
            self.stop_vehicle(address, vehicle_id)

    def process_restart_command(self, address, vehicle_id):
        state = self.get_vehicle_state(vehicle_id)

        if state.last_command == "restart":
            print(f"Vehicle {vehicle_id} is already restarted!")
        else:
            state.last_command = "restart"
            if state.stop_requested:
                print(f"Restarting vehicle {vehicle_id} from the beginning...")
                state.last_stopped_location = None
                state.last_index = 0

            self.restart_vehicle_position(address, vehicle_id)

    def start_vehicle(self, destination_address, vehicle_id):
        state = self.get_vehicle_state(vehicle_id)

        self.change_vehicle_state(vehicle_id, True, False, False)
        sequence_number = 1

        if state.last_stopped_location:
            self.location = state.last_stopped_location
            print(f"Resuming ride from the last stopped location: {self.location}")

        if state.last_index > 0:
            state.last_index -= 1

        for i in range(state.last_index, len(self.coordinates)):
            if state.restart_requested:
                state.last_stopped_location = None
                state.last_index = 0
                break

            if state.stop_requested:
                state.last_stopped_location = self.location
                state.last_index = i
                break

            coordinate = self.coordinates[i]
            self.location = {
                "latitude": coordinate[0],
                "longitude": coordinate[1]
            }
            print(f"Vehicle {vehicle_id} is driving and currently at: {self.location}")

            self.UDPServerSocket.sendto(f"Location: {self.location}".encode("utf-8"), destination_address)
            data = {'latitude': self.location["latitude"], 'longitude': self.location["longitude"]}
            self.firebaseManager.update_vehicle_data(f"{vehicle_id}", data)
            sequence_number += 1

            time.sleep(state.speed)

    def stop_vehicle(self, destination_address, vehicle_id):
        state = self.get_vehicle_state(vehicle_id)

        self.change_vehicle_state(vehicle_id, False, True, False)
        self.UDPServerSocket.sendto(f"Vehicle {vehicle_id} stopped!".encode("utf-8"), destination_address)

    def restart_vehicle_position(self, destination_address, vehicle_id):
        state = self.get_vehicle_state(vehicle_id)

        self.change_vehicle_state(vehicle_id, False, True, True)

        coordinate = self.coordinates[0]
        self.location = {
            "latitude": coordinate[0],
            "longitude": coordinate[1]
        }

        state.last_command = "restart"
        self.UDPServerSocket.sendto(f"Location: {self.location}".encode("utf-8"), destination_address)

        data = {'latitude': self.location["latitude"], 'longitude': self.location["longitude"]}
        self.firebaseManager.update_vehicle_data(f"{vehicle_id}", data)

    def receive_commands(self):
        while True:
            bytes_address_pair = self.UDPServerSocket.recvfrom(1024)
            message = bytes_address_pair[0].decode("utf-8")
            address = bytes_address_pair[1]

            parts = message.split(' ')
            print(parts)
            if len(parts) != 2:
                continue

            command, vehicle_id = parts
            command = command.lower()

            command_switch = {
                "start": self.process_start_command,
                "stop": self.process_stop_command,
                "restart": self.process_restart_command,
                "current-position": self.send_current_location,
            }

            # Pass both command and vehicle ID to the corresponding handler
            command_switch.get(command, lambda _: None)(address, vehicle_id)

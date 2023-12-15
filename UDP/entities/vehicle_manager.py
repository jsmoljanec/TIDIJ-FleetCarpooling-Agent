import socket
import threading
import time
import os
from dotenv import load_dotenv

from .firebase_admin_manager import FirebaseAdminManager
from .google_maps import GoogleMapsAPI
from .strings import Strings
from .vehicle_state import VehicleState

load_dotenv()
firebase_credentials_path = os.getenv("CREDENTIALS_PATH")
firebase_database_url = os.getenv("DATABASE_URL")
firebaseManager = FirebaseAdminManager(firebase_credentials_path, firebase_database_url)
maps_api = GoogleMapsAPI()


class VehicleManager:
    def __init__(self, device, port=50001):
        self.coordinates = []
        self.UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            self.UDPServerSocket.bind((device, port))
            print(Strings.AGENT_UP.format(device, port))
            print(Strings.MESSAGE_SEPARATOR)
        except socket.error as e:
            print(Strings.ERROR_UDP_BINDING.format(e))
            raise e

        self.vehicle_states = {}

    def get_vehicle_state(self, vehicle_id):
        if vehicle_id not in self.vehicle_states:
            self.vehicle_states[vehicle_id] = VehicleState(vehicle_id)
            self.vehicle_states[vehicle_id].set_location(firebaseManager.get_vehicle_current_position(vehicle_id))
        return self.vehicle_states[vehicle_id]

    def change_vehicle_state(self, vehicle_id, is_running, stop_requested, restart_requested):
        state = self.get_vehicle_state(vehicle_id)
        state.is_running = is_running
        state.stop_requested = stop_requested
        state.restart_requested = restart_requested

    def change_vehicle_route(self, vehicle_id, destination):
        state = self.get_vehicle_state(vehicle_id)
        current_location = firebaseManager.get_vehicle_current_position(vehicle_id)
        coordinates = GoogleMapsAPI.get_directions(GoogleMapsAPI(),
                                                   f"{current_location['latitude']}, {state.location['longitude']}",
                                                   destination)
        if len(coordinates) > 0:
            state.set_route(coordinates)
        else:
            print(Strings.ERROR_LOCATION_FIND.format(destination, vehicle_id))

    def send_current_location(self, address, vehicle_id):
        state = self.get_vehicle_state(vehicle_id)
        self.UDPServerSocket.sendto(Strings.VEHICLE_CURRENT_LOCATION.format(vehicle_id, state.location).encode("utf-8"), address)
        print(Strings.VEHICLE_CURRENT_LOCATION.format(vehicle_id, state.location))

    def process_start_command(self, address, vehicle_id):
        state = self.get_vehicle_state(vehicle_id)

        if len(state.coordinates) != 0:
            if state.is_running or state.last_command == Strings.START_COMMAND:
                print(Strings.VEHICLE_ALREADY_RUNNING.format(vehicle_id))
            else:
                print(Strings.VEHICLE_STARTED.format(vehicle_id))
                state.last_command = Strings.START_COMMAND
                vehicle_thread = threading.Thread(target=self.start_vehicle, args=(address, vehicle_id))
                vehicle_thread.start()
        else:
            print(Strings.VEHICLE_NO_DESTINATION.format(state.vehicle_id))

    def process_stop_command(self, address, vehicle_id):
        state = self.get_vehicle_state(vehicle_id)

        if not state.is_running or state.last_command == Strings.STOP_COMMAND:
            print(Strings.VEHICLE_NOT_RUNNING.format(vehicle_id))
        else:
            print(Strings.VEHICLE_STOPPED.format(vehicle_id))
            state.last_command = Strings.STOP_COMMAND
            self.stop_vehicle(address, vehicle_id)

    def process_restart_command(self, address, vehicle_id):
        state = self.get_vehicle_state(vehicle_id)

        if not state.coordinates:
            print(Strings.VEHICLE_CANNOT_RESTART.format(vehicle_id))
            return

        if state.last_command == Strings.RESTART_COMMAND:
            print(Strings.VEHICLE_ALREADY_RESTARTED.format(vehicle_id))
        else:
            state.last_command = Strings.RESTART_COMMAND
            if state.stop_requested:
                print(Strings.VEHICLE_RESTARTED.format(vehicle_id))
                state.last_stopped_location = None
                state.last_index = 0

            self.restart_vehicle_position(address, vehicle_id)

    def process_set_destination(self, destination_address, vehicle_id, destination):
        state = self.get_vehicle_state(vehicle_id)

    def start_vehicle(self, destination_address, vehicle_id):
        state = self.get_vehicle_state(vehicle_id)

        self.change_vehicle_state(vehicle_id, True, False, False)
        sequence_number = 1

        if state.last_stopped_location:
            state.location = state.last_stopped_location
            print(Strings.VEHICLE_RESUMED.format(state.location))

        if state.last_index > 0:
            state.last_index -= 1

        for i in range(state.last_index, len(state.coordinates)):
            if state.restart_requested:
                state.last_stopped_location = None
                state.last_index = 0
                break

            if state.stop_requested:
                state.last_stopped_location = state.location
                state.last_index = i
                break

            coordinate = state.coordinates[i]
            state.location = {
                "latitude": coordinate[0],
                "longitude": coordinate[1]
            }
            print(Strings.VEHICLE_DRIVING_LOCATION.format(vehicle_id, state.location))
            self.UDPServerSocket.sendto(Strings.VEHICLE_CURRENT_LOCATION.format(vehicle_id, state.location).encode("utf-8"), destination_address)
            data = {'latitude': state.location["latitude"], 'longitude': state.location["longitude"]}
            firebaseManager.update_vehicle_data(f"{vehicle_id}", data)
            sequence_number += 1

            time.sleep(state.speed)

    def stop_vehicle(self, destination_address, vehicle_id):
        self.change_vehicle_state(vehicle_id, False, True, False)
        self.UDPServerSocket.sendto(Strings.VEHICLE_STOPPED.format(vehicle_id).encode("utf-8"), destination_address)

    def restart_vehicle_position(self, destination_address, vehicle_id):
        state = self.get_vehicle_state(vehicle_id)

        self.change_vehicle_state(vehicle_id, False, True, True)

        coordinate = state.coordinates[0]
        state.location = {
            "latitude": coordinate[0],
            "longitude": coordinate[1]
        }

        state.last_command = Strings.RESTART_COMMAND
        self.UDPServerSocket.sendto(Strings.VEHICLE_CURRENT_LOCATION.format(vehicle_id, state.location).encode("utf-8"), destination_address)

        data = {'latitude': state.location["latitude"], 'longitude': state.location["longitude"]}
        firebaseManager.update_vehicle_data(f"{vehicle_id}", data)

    def receive_commands(self):
        while True:
            bytes_address_pair = self.UDPServerSocket.recvfrom(1024)
            message = bytes_address_pair[0].decode("utf-8")
            address = bytes_address_pair[1]

            parts = message.split(' ')
            # print(parts)
            if len(parts) == 2:
                command, vehicle_id = parts
                command = command.lower()

                command_switch = {
                    Strings.START_COMMAND: self.process_start_command,
                    Strings.STOP_COMMAND: self.process_stop_command,
                    Strings.RESTART_COMMAND: self.process_restart_command,
                    Strings.CURRENT_POSITION_COMMAND: self.send_current_location,
                }

                # Pass both command and vehicle ID to the corresponding handler
                command_switch.get(command, lambda _: None)(address, vehicle_id)
            elif len(parts) == 3:
                command, destination, vehicle_id = parts
                command = command.lower()

                if command == Strings.SET_DESTINATION_COMMAND:
                    self.change_vehicle_route(vehicle_id, destination)

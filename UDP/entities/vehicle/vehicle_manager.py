import threading
import time
from datetime import datetime

from UDP.entities.utilities.strings import Strings
from UDP.entities.vehicle.vehicle_state import VehicleState
from UDP.entities.vehicle.vehicle_id_extractor import VehicleIdExtractor


class VehicleManager:
    def __init__(self, udp_server, firebase_manager, maps_api, vehicle_statistics):
        self.udp_server = udp_server
        self.firebase_manager = firebase_manager
        self.maps_api = maps_api
        self.vehicle_statistics = vehicle_statistics

        self.vehicle_states = {}

    def initialize_vehicle(self, vehicle_id):
        extracted_vehicle_id = VehicleIdExtractor.extract_vehicle_id(vehicle_id)
        vehicle = self.firebase_manager.vehicles_manager.get_all_vehicle_data(extracted_vehicle_id)
        vehicle_location = self.firebase_manager.vehicle_locations_manager.get_all_vehicle_location_data(extracted_vehicle_id)
        self.vehicle_states[vehicle_id] = VehicleState(vehicle_id)
        self.vehicle_states[vehicle_id].set_reservation_id(
            self.firebase_manager.reservations_manager.get_current_reservation_for_vin_car(extracted_vehicle_id)[0]['reservation_id'])
        self.vehicle_states[vehicle_id].set_firebase_id(extracted_vehicle_id)
        self.vehicle_states[vehicle_id].set_location(
            {"latitude": vehicle_location["latitude"], "longitude": vehicle_location["longitude"]})
        self.vehicle_states[vehicle_id].set_vehicle_lock_status(vehicle_location['locked'])
        self.vehicle_states[vehicle_id].set_fuel_consumption(vehicle['fuelConsumption'])

    def get_vehicle_state(self, vehicle_id):
        if vehicle_id not in self.vehicle_states:
            self.initialize_vehicle(vehicle_id)
        return self.vehicle_states[vehicle_id]

    def get_all_vehicle_states(self):
        return self.vehicle_states

    def change_vehicle_route(self, vehicle_id, destination, address):
        state = self.get_vehicle_state(vehicle_id)
        current_location = self.firebase_manager.vehicle_locations_manager.get_vehicle_current_position(state.firebase_id)
        destination = destination.replace('_', ' ')
        coordinates = self.maps_api.get_directions(f"{current_location['latitude']}, {state.location['longitude']}",
                                                   destination)
        if len(coordinates) > 0:
            state.set_route(coordinates)
            print(Strings.VEHICLE_ROUTE_SET.format(vehicle_id, destination))
            self.udp_server.send_udp_message(Strings.VEHICLE_ROUTE_SET.format(vehicle_id, destination), address)

        else:
            print(Strings.ERROR_LOCATION_FIND.format(destination, vehicle_id))
            self.udp_server.send_udp_message(Strings.ERROR_LOCATION_FIND.format(destination, vehicle_id), address)

    def send_current_location(self, address, vehicle_id):
        state = self.get_vehicle_state(vehicle_id)
        self.udp_server.send_udp_message(Strings.VEHICLE_CURRENT_LOCATION.format(vehicle_id, state.location), address)
        print(Strings.VEHICLE_CURRENT_LOCATION.format(vehicle_id, state.location))

    def process_start_command(self, address, vehicle_id):
        state = self.get_vehicle_state(vehicle_id)

        if state.is_vehicle_locked() is not True:
            if state.is_destination_set():
                if state.is_vehicle_running():
                    print(Strings.VEHICLE_ALREADY_RUNNING.format(vehicle_id))
                    self.udp_server.send_udp_message(Strings.VEHICLE_ALREADY_RUNNING.format(vehicle_id), address)
                else:
                    print(Strings.VEHICLE_STARTED.format(vehicle_id))
                    self.udp_server.send_udp_message(Strings.VEHICLE_STARTED.format(vehicle_id), address)
                    state.remember_vehicle_last_command(Strings.START_COMMAND)
                    vehicle_thread = threading.Thread(target=self.start_vehicle, args=(address, vehicle_id))
                    vehicle_thread.start()
            else:
                print(Strings.VEHICLE_NO_DESTINATION.format(state.vehicle_id))
                self.udp_server.send_udp_message(Strings.VEHICLE_NO_DESTINATION.format(state.vehicle_id), address)
        else:
            print(Strings.VEHICLE_CANT_START_LOCKED.format(state.vehicle_id))
            self.udp_server.send_udp_message(Strings.VEHICLE_CANT_START_LOCKED.format(state.vehicle_id), address)

    def process_stop_command(self, address, vehicle_id):
        state = self.get_vehicle_state(vehicle_id)

        if state.is_vehicle_stopped():
            print(Strings.VEHICLE_NOT_RUNNING.format(vehicle_id))
            self.udp_server.send_udp_message(Strings.VEHICLE_NOT_RUNNING.format(vehicle_id), address)
        else:
            print(Strings.VEHICLE_STOPPED.format(vehicle_id))
            state.remember_vehicle_last_command(Strings.STOP_COMMAND)
            self.stop_vehicle(address, vehicle_id)
            self.udp_server.send_udp_message(Strings.VEHICLE_STOPPED.format(vehicle_id), address)

    def process_restart_command(self, address, vehicle_id):
        state = self.get_vehicle_state(vehicle_id)

        if not state.is_destination_set():
            print(Strings.VEHICLE_CANNOT_RESTART.format(vehicle_id))
            self.udp_server.send_udp_message(Strings.VEHICLE_CANNOT_RESTART.format(vehicle_id), address)
            return

        if not state.is_vehicle_locked():
            if state.is_vehicle_restarted():
                print(Strings.VEHICLE_ALREADY_RESTARTED.format(vehicle_id))
                self.udp_server.send_udp_message(Strings.VEHICLE_ALREADY_RESTARTED.format(vehicle_id), address)
            else:
                state.remember_vehicle_last_command(Strings.RESTART_COMMAND)
                if state.stop_requested:
                    print(Strings.VEHICLE_RESTARTED.format(vehicle_id))
                    self.udp_server.send_udp_message(Strings.VEHICLE_RESTARTED.format(vehicle_id), address)
                    state.last_stopped_location = None
                    state.last_index = 0

                self.restart_vehicle_position(address, vehicle_id)
        else:
            print(Strings.VEHICLE_CANT_BE_RESTARTED.format(vehicle_id))
            self.udp_server.send_udp_message(Strings.VEHICLE_CANT_BE_RESTARTED.format(vehicle_id), address)

    def process_lock_command(self, address, vehicle_id):
        state = self.get_vehicle_state(vehicle_id)
        if state.is_vehicle_locked():
            state.set_vehicle_lock_status(False)
            data = {'locked': False}
        else:
            state.set_vehicle_lock_status(True)
            data = {'locked': True}
        self.firebase_manager.vehicle_locations_manager.update_vehicle_location_data(f"{state.firebase_id}", data)
        check_string = Strings.VEHICLE_LOCKED.format(
            vehicle_id) if state.locked is True else Strings.VEHICLE_UNLOCKED.format(vehicle_id)
        print(check_string)
        self.udp_server.send_udp_message(check_string, address)

    def driving_vehicle(self, state, vehicle_id, address):
        state.check_index()
        for i in range(state.last_index, len(state.coordinates)):
            if state.restart_requested:
                state.last_stopped_location = None
                state.last_index = 0
                break

            if state.stop_requested:
                state.last_stopped_location = state.location
                state.last_index = i
                break

            previous_location = state.get_location()
            coordinate = state.coordinates[i]
            state.set_location({"latitude": coordinate[0], "longitude": coordinate[1]})

            print(Strings.VEHICLE_DRIVING_LOCATION.format(vehicle_id, state.location))
            self.udp_server.send_udp_message(Strings.VEHICLE_CURRENT_LOCATION.format(vehicle_id, state.location),
                                             address)
            data = state.get_location()
            self.firebase_manager.vehicle_locations_manager.update_vehicle_location_data(f"{state.firebase_id}", data)
            distance_between_two_points = self.vehicle_statistics.calculate_distance(previous_location, state.location)
            fuel_consumption = self.vehicle_statistics.calculate_random_fuel_consumption(distance_between_two_points,
                                                                                         state.nominal_fuel_consumption)
            state.distance_traveled = state.distance_traveled + distance_between_two_points
            state.combined_fuel_consumption = state.combined_fuel_consumption + fuel_consumption
            print(
                f"Distance traveled so far: {round(state.distance_traveled, 2)} km. Fuel consumed: {round(state.combined_fuel_consumption, 2)} L")
            time.sleep(state.get_vehicle_speed())

    def start_vehicle(self, address, vehicle_id):
        state = self.get_vehicle_state(vehicle_id)
        state.change_vehicle_state(True, False, False)

        if state.last_stopped_location:
            state.set_location(state.last_stopped_location)
            print(Strings.VEHICLE_RESUMED.format(vehicle_id, state.location))
            self.udp_server.send_udp_message(Strings.VEHICLE_RESUMED.format(vehicle_id, state.location), address)

        self.driving_vehicle(state, vehicle_id, address)

    def stop_vehicle(self, address, vehicle_id):
        state = self.get_vehicle_state(vehicle_id)
        state.change_vehicle_state(False, True, False)
        self.udp_server.send_udp_message(Strings.VEHICLE_STOPPED.format(vehicle_id), address)

    def restart_vehicle_position(self, address, vehicle_id):
        state = self.get_vehicle_state(vehicle_id)
        state.change_vehicle_state(False, True, True)

        coordinate = state.coordinates[0]
        state.set_location({"latitude": coordinate[0], "longitude": coordinate[1]})
        state.remember_vehicle_last_command(Strings.RESTART_COMMAND)

        self.udp_server.send_udp_message(Strings.VEHICLE_RESTARTED.format(vehicle_id), address)

        data = state.get_location()
        self.firebase_manager.vehicle_locations_manager.update_vehicle_location_data(f"{state.firebase_id}", data)

    def store_all_vehicle_distance_data(self):
        for vehicle, value in self.get_all_vehicle_states().items():
            distance_traveled_local = int(value.distance_traveled)
            fuel_consumption_local = value.combined_fuel_consumption
            print(f"Vehicle: {vehicle}, Distance traveled: {distance_traveled_local}")
            distance_traveled_firebase = self.firebase_manager.vehicles_manager.get_vehicle_traveled_distance(value.firebase_id)
            fuel_consumption_firebase = self.firebase_manager.reservations_manager.get_reservation_fuel_consumption(value.reservation_id)
            total_distance = distance_traveled_firebase + distance_traveled_local
            total_fuel_consumption = round(fuel_consumption_firebase + fuel_consumption_local, 2)
            data = {'distanceTraveled': total_distance}
            self.firebase_manager.vehicles_manager.update_vehicle_data(f"{value.firebase_id}", data)
            data = {'fuelConsumption': total_fuel_consumption}
            self.firebase_manager.reservations_manager.update_reservation_data(f"{value.reservation_id}", data)

    def refine_vehicle_id(self, vehicle_id):
        reservation = self.firebase_manager.reservations_manager.get_current_reservation_for_vin_car(vehicle_id)

        pickup_date_time_raw = datetime.strptime(f"{reservation[0]['pickupDate']} {reservation[0]['pickupTime']}",
                                                 "%Y-%m-%d %H:%M")
        pickup_date_time_number = int((pickup_date_time_raw - datetime(1970, 1, 1)).total_seconds() / 60)
        return_date_time_raw = datetime.strptime(f"{reservation[0]['returnDate']} {reservation[0]['returnTime']}",
                                                 "%Y-%m-%d %H:%M")
        return_date_time_number = int((return_date_time_raw - datetime(1970, 1, 1)).total_seconds() / 60)

        return f"{vehicle_id}-{pickup_date_time_number}-{return_date_time_number}"

    def check_if_there_is_initiated_reservation_ongoing(self, vehicle_id):
        current_datetime = datetime.now()
        current_datetime_number = (current_datetime - datetime(1970, 1, 1)).total_seconds() / 60

        all_vehicles = self.get_all_vehicle_states()
        for key, value in all_vehicles.items():
            if key.startswith(vehicle_id):
                input_string = key
                parts = input_string.split('-')

                if len(parts) >= 3:
                    pickup_date_time_number = int(parts[1])
                    return_date_time_number = int(parts[2])
                    if pickup_date_time_number <= current_datetime_number <= return_date_time_number:
                        return key

        return self.refine_vehicle_id(vehicle_id)

    def process_udp_message(self, message, address):
        parts = message.split(' ')
        if len(parts) == 2:
            command, vehicle_id = parts
            command = command.lower()

            vehicle_id = self.refine_vehicle_id(vehicle_id)

            command_switch = {
                Strings.START_COMMAND: self.process_start_command,
                Strings.STOP_COMMAND: self.process_stop_command,
                Strings.RESTART_COMMAND: self.process_restart_command,
                Strings.CURRENT_POSITION_COMMAND: self.send_current_location,
                Strings.LOCK_COMMAND: self.process_lock_command
            }

            command_switch.get(command, lambda _: None)(address, vehicle_id)
        elif len(parts) == 3:
            command, destination, vehicle_id = parts
            command = command.lower()

            if command == Strings.SET_DESTINATION_COMMAND:
                check_vehicle_id = self.check_if_there_is_initiated_reservation_ongoing(vehicle_id)
                self.change_vehicle_route(check_vehicle_id, destination, address)

    def receive_commands(self):
        self.udp_server.receive_commands(self)

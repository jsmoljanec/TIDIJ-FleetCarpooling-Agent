import threading
import time

from UDP.entities.utilities.reservation_utils import ReservationUtils
from UDP.entities.utilities.strings import Strings
from UDP.entities.vehicle.vehicle_state import VehicleState
from UDP.entities.utilities.vehicle_id_extractor import VehicleIdExtractor


class VehicleManager:
    def __init__(self, udp_server, firebase_manager, maps_api, vehicle_statistics):
        self.udp_server = udp_server
        self.firebase_manager = firebase_manager
        self.maps_api = maps_api
        self.vehicle_statistics = vehicle_statistics
        self.reservation_utils = ReservationUtils(self.firebase_manager)

        self.vehicle_states = {}

    def initialize_vehicle(self, vehicle_id):
        extracted_vehicle_id = VehicleIdExtractor.extract_vehicle_id(vehicle_id)
        vehicle = self.firebase_manager.vehicles_manager.get_all_vehicle_data(extracted_vehicle_id)
        vehicle_location = self.firebase_manager.vehicle_locations_manager.get_all_vehicle_location_data(
            extracted_vehicle_id)
        self.vehicle_states[vehicle_id] = VehicleState(vehicle_id)
        self.vehicle_states[vehicle_id].firebase_identification.set_reservation_id(
            self.firebase_manager.reservations_manager.get_current_reservation_for_vin_car(extracted_vehicle_id)[0][
                'reservation_id'])
        self.vehicle_states[vehicle_id].firebase_identification.set_firebase_id(extracted_vehicle_id)
        self.vehicle_states[vehicle_id].location_details.set_location(
            {"latitude": vehicle_location["latitude"], "longitude": vehicle_location["longitude"]})
        self.vehicle_states[vehicle_id].status_and_controls.update_vehicle_lock_status(vehicle_location['locked'])
        self.vehicle_states[vehicle_id].vehicle_data.set_fuel_consumption(vehicle['fuelConsumption'])

    def get_vehicle_state(self, vehicle_id):
        if vehicle_id not in self.vehicle_states:
            self.initialize_vehicle(vehicle_id)
        return self.vehicle_states[vehicle_id]

    def get_all_vehicle_states(self):
        return self.vehicle_states

    def change_vehicle_route(self, vehicle_id, destination, address):
        state = self.get_vehicle_state(vehicle_id)
        current_location = self.firebase_manager.vehicle_locations_manager.get_vehicle_current_position(
            state.firebase_identification.firebase_id)
        destination = destination.replace('_', ' ')
        coordinates = self.maps_api.get_directions(f"{current_location['latitude']}, {state.location_details.location['longitude']}",
                                                   destination)
        if len(coordinates) > 0:
            state.location_details.set_route(coordinates)
            print(Strings.VEHICLE_ROUTE_SET.format(vehicle_id, destination))
            self.udp_server.send_udp_message(Strings.VEHICLE_ROUTE_SET.format(vehicle_id, destination), address)

        else:
            print(Strings.ERROR_LOCATION_FIND.format(destination, vehicle_id))
            self.udp_server.send_udp_message(Strings.ERROR_LOCATION_FIND.format(destination, vehicle_id), address)

    def send_current_location(self, address, vehicle_id):
        state = self.get_vehicle_state(vehicle_id)
        self.udp_server.send_udp_message(Strings.VEHICLE_CURRENT_LOCATION.format(vehicle_id, state.location_details.location), address)
        print(Strings.VEHICLE_CURRENT_LOCATION.format(vehicle_id, state.location_details.location))

    def process_start_command(self, address, vehicle_id):
        state = self.get_vehicle_state(vehicle_id)

        if state.status_and_controls.is_vehicle_locked() is not True:
            if state.location_details.is_destination_set():
                if state.status_and_controls.is_vehicle_running():
                    print(Strings.VEHICLE_ALREADY_RUNNING.format(vehicle_id))
                    self.udp_server.send_udp_message(Strings.VEHICLE_ALREADY_RUNNING.format(vehicle_id), address)
                else:
                    print(Strings.VEHICLE_STARTED.format(vehicle_id))
                    self.udp_server.send_udp_message(Strings.VEHICLE_STARTED.format(vehicle_id), address)
                    state.status_and_controls.remember_vehicle_last_command(Strings.START_COMMAND)
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

        if state.status_and_controls.is_vehicle_stopped():
            print(Strings.VEHICLE_NOT_RUNNING.format(vehicle_id))
            self.udp_server.send_udp_message(Strings.VEHICLE_NOT_RUNNING.format(vehicle_id), address)
        else:
            print(Strings.VEHICLE_STOPPED.format(vehicle_id))
            state.status_and_controls.remember_vehicle_last_command(Strings.STOP_COMMAND)
            self.stop_vehicle(address, vehicle_id)
            self.udp_server.send_udp_message(Strings.VEHICLE_STOPPED.format(vehicle_id), address)

    def process_restart_command(self, address, vehicle_id):
        state = self.get_vehicle_state(vehicle_id)

        if not state.location_details.is_destination_set():
            print(Strings.VEHICLE_CANNOT_RESTART.format(vehicle_id))
            self.udp_server.send_udp_message(Strings.VEHICLE_CANNOT_RESTART.format(vehicle_id), address)
            return

        if not state.status_and_controls.is_vehicle_locked():
            if state.status_and_controls.is_vehicle_restarted():
                print(Strings.VEHICLE_ALREADY_RESTARTED.format(vehicle_id))
                self.udp_server.send_udp_message(Strings.VEHICLE_ALREADY_RESTARTED.format(vehicle_id), address)
            else:
                state.status_and_controls.remember_vehicle_last_command(Strings.RESTART_COMMAND)
                if state.status_and_controls.stop_requested:
                    print(Strings.VEHICLE_RESTARTED.format(vehicle_id))
                    self.udp_server.send_udp_message(Strings.VEHICLE_RESTARTED.format(vehicle_id), address)
                    state.location_details.last_stopped_location = None
                    state.location_details.last_index = 0

                self.restart_vehicle_position(address, vehicle_id)
        else:
            print(Strings.VEHICLE_CANT_BE_RESTARTED.format(vehicle_id))
            self.udp_server.send_udp_message(Strings.VEHICLE_CANT_BE_RESTARTED.format(vehicle_id), address)

    def process_lock_command(self, address, vehicle_id):
        state = self.get_vehicle_state(vehicle_id)

        is_locked = state.status_and_controls.is_vehicle_locked()
        state.status_and_controls.update_vehicle_lock_status(not is_locked)
        data = {'locked': not is_locked}

        self.lock_vehicle(state, vehicle_id, address, data)

    def lock_vehicle(self, state, vehicle_id, address, data):
        self.firebase_manager.vehicle_locations_manager.update_vehicle_location_data(f"{state.firebase_identification.firebase_id}", data)

        check_string = Strings.VEHICLE_LOCKED.format(
            vehicle_id) if state.status_and_controls.locked is True else Strings.VEHICLE_UNLOCKED.format(vehicle_id)
        print(check_string)

        self.udp_server.send_udp_message(check_string, address)

    def driving_vehicle(self, state, vehicle_id, address):
        state.location_details.check_index()
        for i in range(state.location_details.last_index, len(state.location_details.coordinates)):
            if state.status_and_controls.restart_requested:
                state.location_details.last_stopped_location = None
                state.location_details.last_index = 0
                break

            if state.status_and_controls.stop_requested:
                state.location_details.last_stopped_location = state.location_details.location
                state.location_details.last_index = i
                break

            previous_location = state.location_details.get_location()
            coordinate = state.location_details.coordinates[i]
            state.location_details.set_location({"latitude": coordinate[0], "longitude": coordinate[1]})

            print(Strings.VEHICLE_DRIVING_LOCATION.format(vehicle_id, state.location_details.location))
            self.udp_server.send_udp_message(Strings.VEHICLE_CURRENT_LOCATION.format(vehicle_id, state.location_details.location),
                                             address)
            data = state.location_details.get_location()
            self.firebase_manager.vehicle_locations_manager.update_vehicle_location_data(f"{state.firebase_identification.firebase_id}", data)
            distance_between_two_points = self.vehicle_statistics.calculate_distance(previous_location, state.location_details.location)
            fuel_consumption = self.vehicle_statistics.calculate_random_fuel_consumption(distance_between_two_points,
                                                                                         state.vehicle_data.nominal_fuel_consumption)
            state.distance_traveled = round(state.vehicle_data.distance_traveled + distance_between_two_points, 2)
            state.vehicle_data.combined_fuel_consumption = round(state.vehicle_data.combined_fuel_consumption + fuel_consumption, 2)
            print(f"Distance traveled so far: {state.vehicle_data.distance_traveled} km. Fuel consumed: {state.vehicle_data.combined_fuel_consumption} L")
            time.sleep(state.vehicle_data.get_vehicle_speed())

    def start_vehicle(self, address, vehicle_id):
        state = self.get_vehicle_state(vehicle_id)
        state.status_and_controls.change_vehicle_state(True, False, False)

        if state.location_details.last_stopped_location:
            state.location_details.set_location(state.location_details.last_stopped_location)
            print(Strings.VEHICLE_RESUMED.format(vehicle_id, state.location_details.location))
            self.udp_server.send_udp_message(Strings.VEHICLE_RESUMED.format(vehicle_id, state.location_details.location), address)

        self.driving_vehicle(state, vehicle_id, address)

    def stop_vehicle(self, address, vehicle_id):
        state = self.get_vehicle_state(vehicle_id)
        state.status_and_controls.change_vehicle_state(False, True, False)
        self.udp_server.send_udp_message(Strings.VEHICLE_STOPPED.format(vehicle_id), address)

    def restart_vehicle_position(self, address, vehicle_id):
        state = self.get_vehicle_state(vehicle_id)
        state.status_and_controls.change_vehicle_state(False, True, True)

        coordinate = state.location_details.coordinates[0]
        state.location_details.set_location({"latitude": coordinate[0], "longitude": coordinate[1]})
        state.status_and_controls.remember_vehicle_last_command(Strings.RESTART_COMMAND)

        self.udp_server.send_udp_message(Strings.VEHICLE_RESTARTED.format(vehicle_id), address)

        data = state.location_details.get_location()
        self.firebase_manager.vehicle_locations_manager.update_vehicle_location_data(f"{state.firebase_identification.firebase_id}", data)

    def store_all_vehicle_distance_data(self):
        for vehicle, value in self.get_all_vehicle_states().items():
            distance_traveled_local = int(value.vehicle_data.distance_traveled)
            fuel_consumption_local = value.vehicle_data.combined_fuel_consumption
            print(f"Vehicle: {vehicle}, Distance traveled: {distance_traveled_local}")
            distance_traveled_firebase = self.firebase_manager.vehicles_manager.get_vehicle_traveled_distance(
                value.firebase_identification.firebase_id)
            fuel_consumption_firebase = self.firebase_manager.reservations_manager.get_reservation_fuel_consumption(
                value.firebase_identification.reservation_id)
            total_distance = distance_traveled_firebase + distance_traveled_local
            total_fuel_consumption = round(fuel_consumption_firebase + fuel_consumption_local, 2)
            data = {'distanceTraveled': total_distance}
            self.firebase_manager.vehicles_manager.update_vehicle_data(f"{value.firebase_identification.firebase_id}", data)
            data = {'fuelConsumption': total_fuel_consumption}
            self.firebase_manager.reservations_manager.update_reservation_data(f"{value.firebase_identification.reservation_id}", data)

    def process_udp_message(self, message, address):
        parts = message.split(' ')
        if len(parts) == 2:
            command, vehicle_id = parts
            command = command.lower()

            vehicle_id = self.reservation_utils.create_vehicle_id_from_reservation_dates(vehicle_id)

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
                check_vehicle_id = self.reservation_utils.check_if_there_is_initiated_reservation_ongoing(vehicle_id, self)
                self.change_vehicle_route(check_vehicle_id, destination, address)

    def receive_commands(self):
        self.udp_server.receive_commands(self)

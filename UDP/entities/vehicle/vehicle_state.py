from UDP.entities.utilities.strings import Strings


class VehicleState:
    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        self.is_running = False
        self.stop_requested = False
        self.restart_requested = False
        self.last_stopped_location = None
        self.last_index = 0
        self.last_command = None
        self.speed = 1
        self.coordinates = []
        self.location = None
        self.locked = None
        self.distance_traveled = 0
        self.nominal_fuel_consumption = 0
        self.combined_fuel_consumption = 0
        self.firebase_id = None
        self.reservation_id = None

    def set_route(self, coordinates):
        self.coordinates = coordinates

    def set_location(self, location):
        self.location = location

    def get_location(self):
        return self.location

    def is_vehicle_locked(self):
        return self.locked is True

    def set_vehicle_lock_status(self, lock):
        self.locked = lock

    def set_fuel_consumption(self, fuel_consumption):
        self.nominal_fuel_consumption = fuel_consumption

    def set_firebase_id(self, firebase_id):
        self.firebase_id = firebase_id

    def set_reservation_id(self, reservation_id):
        self.reservation_id = reservation_id

    def is_vehicle_stopped(self):
        return not self.is_running or self.last_command == Strings.STOP_COMMAND

    def is_destination_set(self):
        return len(self.coordinates) > 0

    def is_vehicle_restarted(self):
        return self.last_command == Strings.RESTART_COMMAND

    def is_vehicle_running(self):
        return self.is_running or self.last_command == Strings.START_COMMAND

    def check_index(self):
        if self.last_index > 0:
            self.last_index -= 1

    def get_vehicle_speed(self):
        return self.speed

    def remember_vehicle_last_command(self, command):
        self.last_command = command

    def change_vehicle_state(self, is_running, stop_requested, restart_requested):
        self.is_running = is_running
        self.stop_requested = stop_requested
        self.restart_requested = restart_requested

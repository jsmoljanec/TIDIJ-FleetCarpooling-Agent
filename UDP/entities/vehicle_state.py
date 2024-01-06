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

    def set_route(self, coordinates):
        self.coordinates = coordinates

    def set_location(self, location):
        self.location = location

    def set_vehicle_lock_status(self, lock):
        self.locked = lock

    def is_vehicle_locked(self):
        return self.locked is True

    def set_fuel_consumption(self, fuel_consumption):
        self.nominal_fuel_consumption = fuel_consumption

    def set_firebase_id(self, firebase_id):
        self.firebase_id = firebase_id

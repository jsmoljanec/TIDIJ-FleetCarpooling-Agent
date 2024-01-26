class VehicleData:
    def __init__(self):
        self.speed = 1
        self.distance_traveled = 0
        self.nominal_fuel_consumption = 0
        self.combined_fuel_consumption = 0

    def set_fuel_consumption(self, fuel_consumption):
        self.nominal_fuel_consumption = fuel_consumption

    def get_vehicle_speed(self):
        return self.speed

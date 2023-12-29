import random
from math import radians, sin, cos, sqrt, atan2


class VehicleStatistics:
    def __init__(self):
        self.earth_radius = 6371.0

    def calculate_distance(self, location1, location2):
        lat1 = radians(location1["latitude"])
        lon1 = radians(location1["longitude"])
        lat2 = radians(location2[0])
        lon2 = radians(location2[1])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = self.earth_radius * c
        return distance

    @staticmethod
    def calculate_random_fuel_consumption(distance, fuel_efficiency):
        randomness_factor = random.uniform(0.9, 1.1)  # Random factor between 0.9 and 1.1
        adjusted_fuel_efficiency = fuel_efficiency * randomness_factor

        fuel_consumption = (distance / 100) * adjusted_fuel_efficiency
        return fuel_consumption

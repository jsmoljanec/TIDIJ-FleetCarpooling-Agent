import unittest

from UDP.entities.vehicle.vehicle_statistics import VehicleStatistics


class VehicleStatisticsTest(unittest.TestCase):
    def setUp(self):
        self.vehicle_stats = VehicleStatistics()

    def test_calculate_distance_with_valid_locations_returns_calculated_distance(self):
        location1 = {"latitude": 40.7128, "longitude": -74.0060}  # New York
        location2 = {"latitude": 34.0522, "longitude": -118.2437}  # Los Angeles

        distance = self.vehicle_stats.calculate_distance(location1, location2)
        self.assertGreater(distance, 3900)

    def test_calculate_random_fuel_consumption_with_valid_data_returns_fuel_consumption(self):
        distance = 200
        fuel_efficiency = 10

        fuel_consumption = self.vehicle_stats.calculate_random_fuel_consumption(distance, fuel_efficiency)

        expected_min = distance * fuel_efficiency / 100 * 0.9
        expected_max = distance * fuel_efficiency / 100 * 1.1

        self.assertGreaterEqual(fuel_consumption, expected_min)
        self.assertLessEqual(fuel_consumption, expected_max)

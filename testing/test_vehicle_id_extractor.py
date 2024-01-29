import unittest

from UDP.entities.utilities.vehicle_id_extractor import VehicleIdExtractor


class VehicleIdExtractorTest(unittest.TestCase):
    def test_extract_vehicle_id_from_empty_string_returns_none(self):
        vehicle_id = VehicleIdExtractor().extract_vehicle_id("")
        self.assertEqual(vehicle_id, None)

    def test_extract_vehicle_id_from_full_string_returns_vehicle_id(self):
        vehicle_id = VehicleIdExtractor().extract_vehicle_id("556XYZ789LMN123OP-123412341235-123412341235")
        self.assertEqual(vehicle_id, "556XYZ789LMN123OP")

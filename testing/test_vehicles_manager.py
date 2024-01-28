import unittest
from unittest.mock import MagicMock, patch

from UDP.entities.google.firebase.firebase_admin_manager import FirebaseAdminManager

from dotenv import load_dotenv
import os

load_dotenv("../UDP/entities/.env")
firebase_credentials_path = os.getenv("TESTING_CREDENTIALS_PATH")
firebase_database_url = os.getenv("DATABASE_URL")


class VehiclesManagerTest(unittest.TestCase):
    firebase_manager = FirebaseAdminManager(firebase_credentials_path, firebase_database_url)
    db_reference = "UDP.entities.google.firebase.firebase_admin_manager.db.reference"

    @patch('firebase_admin.initialize_app')
    @patch('firebase_admin.db.reference')
    def test_get_all_vehicle_data_from_random_string_returns_none(self, mock_db_reference, mock_initialize_app):
        fake_data = None
        mock_db_reference.return_value.get.return_value = fake_data
        mock_initialize_app.return_value = MagicMock()
        firebase_manager = FirebaseAdminManager(firebase_credentials_path, firebase_database_url)
        firebase_manager.vehicles_manager.get_all_vehicle_data = MagicMock(return_value=fake_data)
        result = firebase_manager.vehicles_manager.get_all_vehicle_data("random")
        self.assertEqual(result, fake_data)

    @patch('firebase_admin.initialize_app')
    @patch('firebase_admin.db.reference')
    def test_get_all_vehicle_data_from_valid_vehicle_id_returns_vehicle_data(self, mock_db_reference, mock_initialize_app):
        fake_data = {'active': 'true', 'brand': 'Audi', 'capacity': '5', 'registration': 'VZ152DF', 'fuelConsumption': 8, 'model': 'A4 Avant'}
        mock_db_reference.return_value.get.return_value = fake_data
        mock_initialize_app.return_value = MagicMock()
        firebase_manager = FirebaseAdminManager(firebase_credentials_path, firebase_database_url)
        firebase_manager.vehicles_manager.get_all_vehicle_data = MagicMock(return_value=fake_data)
        result = firebase_manager.vehicles_manager.get_all_vehicle_data("556XYZ789LMN123OP")
        self.assertEqual(result, fake_data)

    @patch('firebase_admin.initialize_app')
    @patch('firebase_admin.db.reference')
    def test_get_vehicle_nominal_fuel_consumption_from_valid_vehicle_id_returns_nominal_vehicle_fuel_consumption(self, mock_db_reference, mock_initialize_app):
        fake_data = 8
        mock_db_reference.return_value.get.return_value = fake_data
        mock_initialize_app.return_value = MagicMock()
        firebase_manager = FirebaseAdminManager(firebase_credentials_path, firebase_database_url)
        firebase_manager.vehicles_manager.get_vehicle_nominal_fuel_consumption = MagicMock(return_value=fake_data)
        result = firebase_manager.vehicles_manager.get_vehicle_nominal_fuel_consumption('556XYZ789LMN123OP')
        self.assertEqual(result, fake_data)

    @patch('firebase_admin.initialize_app')
    @patch('firebase_admin.db.reference')
    def test_get_vehicle_traveled_distance_from_valid_vehicle_id_returns_vehicle_traveled_distance(self, mock_db_reference, mock_initialize_app):
        fake_data = 20000
        mock_db_reference.return_value.get.return_value = fake_data
        mock_initialize_app.return_value = MagicMock()
        firebase_manager = FirebaseAdminManager(firebase_credentials_path, firebase_database_url)
        firebase_manager.vehicles_manager.get_vehicle_traveled_distance = MagicMock(return_value=fake_data)
        result = firebase_manager.vehicles_manager.get_vehicle_traveled_distance('556XYZ789LMN123OP')
        self.assertEqual(result, fake_data)

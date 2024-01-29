import unittest
from unittest.mock import MagicMock, patch

from UDP.entities.google.firebase.firebase_admin_manager import FirebaseAdminManager

from dotenv import load_dotenv
import os

load_dotenv("../UDP/entities/.env")
firebase_credentials_path = os.getenv("TESTING_CREDENTIALS_PATH")
firebase_database_url = os.getenv("DATABASE_URL")


@patch('firebase_admin.initialize_app')
@patch('firebase_admin.db.reference')
class VehicleLocationsManagerTest(unittest.TestCase):
    db_reference = "UDP.entities.google.firebase.firebase_admin_manager.db.reference"

    def test_get_vehicle_current_position_from_invalid_vehicle_id_returns_no_location(self, mock_db_reference, mock_initialize_app):
        fake_data = None
        mock_db_reference.return_value.get.return_value = fake_data
        mock_initialize_app.return_value = MagicMock()
        firebase_manager = FirebaseAdminManager(firebase_credentials_path, firebase_database_url)
        firebase_manager.vehicle_locations_manager.get_vehicle_current_position = MagicMock(return_value=fake_data)
        result = firebase_manager.vehicle_locations_manager.get_vehicle_current_position("random")
        self.assertEqual(result, fake_data)

    def test_get_vehicle_current_position_from_valid_vehicle_id_returns_location(self, mock_db_reference, mock_initialize_app):
        fake_data = {'latitude': 20, 'longitude': 15}
        mock_db_reference.return_value.get.return_value = fake_data
        mock_initialize_app.return_value = MagicMock()
        firebase_manager = FirebaseAdminManager(firebase_credentials_path, firebase_database_url)
        firebase_manager.vehicle_locations_manager.get_vehicle_current_position = MagicMock(return_value=fake_data)
        result = firebase_manager.vehicle_locations_manager.get_vehicle_current_position("556XYZ789LMN123OP")
        self.assertEqual(result, fake_data)

    def test_get_all_vehicle_location_data_from_invalid_vehicle_id_returns_no_location_data(self, mock_db_reference, mock_initialize_app):
        fake_data = None
        mock_db_reference.return_value.get.return_value = fake_data
        mock_initialize_app.return_value = MagicMock()
        firebase_manager = FirebaseAdminManager(firebase_credentials_path, firebase_database_url)
        firebase_manager.vehicle_locations_manager.get_all_vehicle_location_data = MagicMock(return_value=fake_data)
        result = firebase_manager.vehicle_locations_manager.get_all_vehicle_location_data("556XYZ789LMN123OP")
        self.assertEqual(result, fake_data)

    def test_get_all_vehicle_location_data_from_valid_vehicle_id_returns_all_location_data(self, mock_db_reference, mock_initialize_app):
        fake_data = {'latitude': 20, 'longitude': 15, 'locked': True, 'active': True}
        mock_db_reference.return_value.get.return_value = fake_data
        mock_initialize_app.return_value = MagicMock()
        firebase_manager = FirebaseAdminManager(firebase_credentials_path, firebase_database_url)
        firebase_manager.vehicle_locations_manager.get_all_vehicle_location_data = MagicMock(return_value=fake_data)
        result = firebase_manager.vehicle_locations_manager.get_all_vehicle_location_data("556XYZ789LMN123OP")
        self.assertEqual(result, fake_data)



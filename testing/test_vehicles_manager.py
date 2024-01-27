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

    @patch(db_reference, new_callable=MagicMock)
    def test_get_all_vehicle_data_from_random_string_returns_none(self, mock_db_reference):
        mock_db_reference.child.return_value.get.return_value = {}
        firebase_admin_manager = self.firebase_manager
        result = firebase_admin_manager.vehicles_manager.get_all_vehicle_data('random')
        self.assertEqual(result, None)

    @patch(db_reference, new_callable=MagicMock)
    def test_get_all_vehicle_data_from_valid_vehicle_id_returns_vehicle_data(self, mock_db_reference):
        mock_db_reference.child.return_value.get.return_value = {'active': True, 'brand': 'Audi', 'capacity': 5}
        firebase_admin_manager = self.firebase_manager
        result = firebase_admin_manager.vehicles_manager.get_all_vehicle_data('556XYZ789LMN123OP')
        self.assertEqual([result['registration'], result['brand']], ['VZ152DF', 'Audi'])

    @patch(db_reference, new_callable=MagicMock)
    def test_get_vehicle_nominal_fuel_consumption_from_valid_vehicle_id_returns_nominal_vehicle_fuel_consumption(self, mock_db_reference):
        mock_db_reference.child.return_value.get.return_value = 8
        firebase_admin_manager = self.firebase_manager
        result = firebase_admin_manager.vehicles_manager.get_vehicle_nominal_fuel_consumption('556XYZ789LMN123OP')
        self.assertEqual(result, 8)

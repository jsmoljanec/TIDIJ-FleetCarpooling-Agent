import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from UDP.entities.google.firebase.reservations_manager import ReservationsManager
from UDP.entities.google.firebase.vehicle_location_manager import VehicleLocationsManager
from UDP.entities.google.firebase.vehicles_manager import VehiclesManager
from UDP.entities.utilities.strings import Strings


class FirebaseAdminManager:
    def __init__(self, credentials_path, database_url):
        try:
            cred = credentials.Certificate(credentials_path)
            firebase_admin.initialize_app(cred, {'databaseURL': database_url})
            self.db_reference = db.reference()
        except Exception as e:
            print(Strings.ERROR_FIREBASE.format(e))
            raise e

        self.vehicles_manager = VehiclesManager(self.db_reference)
        self.reservations_manager = ReservationsManager(self.db_reference)
        self.vehicle_locations_manager = VehicleLocationsManager(self.db_reference)

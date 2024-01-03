import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from .strings import Strings


class FirebaseAdminManager:
    def __init__(self, credentials_path, database_url):
        try:
            cred = credentials.Certificate(credentials_path)
            firebase_admin.initialize_app(cred, {'databaseURL': database_url})
            self.db_reference = db.reference()
        except Exception as e:
            print(Strings.ERROR_FIREBASE.format(e))
            raise e

    def get_all_vehicle_data(self):
        try:
            return self.db_reference.child('Vehicles').get()
        except Exception as e:
            print(Strings.ERROR_FIREBASE_GET_VEHICLE_DATA.format(e))
            raise e

    def update_vehicle_data(self, vehicle_id, data):
        try:
            self.db_reference.child(f'Vehicles/{vehicle_id}').update(data)
        except Exception as e:
            print(Strings.ERROR_FIREBASE_UPDATE_VEHICLE_DATA.format(e))
            raise e

    def get_vehicle_current_position(self, vehicle_id):
        try:
            vehicle_data = self.db_reference.child(f'Vehicles/{vehicle_id}').get()
            return {
                "latitude": vehicle_data.get("latitude", 0.0),
                "longitude": vehicle_data.get("longitude", 0.0)
            }
        except Exception as e:
            print(Strings.ERROR_FIREBASE_GET_VEHICLE_LOCATION.format(e))
            raise e

    def get_vehicle_lock_status(self, vehicle_id):
        try:
            vehicle_data = self.db_reference.child(f'Vehicles/{vehicle_id}').get()
            return {
                "locked": vehicle_data.get("locked", 0.0)
            }
        except Exception as e:
            print(Strings.ERROR_FIREBASE_GET_VEHICLE_LOCK_STATUS.format(e))
            raise e

    def get_vehicle_traveled_distance(self, vehicle_id):
        try:
            vehicle_data = self.db_reference.child(f'Vehicles/{vehicle_id}').get()
            return vehicle_data.get("distanceTraveled", 0.0)

        except Exception as e:
            print(Strings.ERROR_FIREBASE_GET_VEHICLE_TRAVELED_DISTANCE.format(e))
            raise e

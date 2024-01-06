import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime

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

    def get_vehicle_nominal_fuel_consumption(self, vehicle_id):
        try:
            vehicle_data = self.db_reference.child(f'Vehicles/{vehicle_id}').get()
            return vehicle_data.get("fuelConsumption", 0.0)

        except Exception as e:
            print(Strings.ERROR_FIREBASE_GET_VEHICLE_FUEL_CONSUMPTION.format(e))
            raise e

    def get_current_reservation_for_vin_car(self, vehicle_id):
        try:
            reservations = self.db_reference.child('Reservation').get()
            current_time = datetime.now()

            matching_reservations = []

            for reservation_id, reservation_data in reservations.items():
                car_vin = reservation_data.get("VinCar", "")
                start_datetime = datetime.strptime(
                    reservation_data.get("pickupDate") + " " + reservation_data.get("pickupTime"), "%Y-%m-%d %H:%M")
                end_datetime = datetime.strptime(
                    reservation_data.get("returnDate") + " " + reservation_data.get("returnTime"), "%Y-%m-%d %H:%M")

                if car_vin == vehicle_id and start_datetime <= current_time <= end_datetime:
                    matching_reservations.append({
                        "reservation_id": reservation_id,
                        "VinCar": car_vin,
                        "pickupDate": reservation_data.get("pickupDate", ""),
                        "pickupTime": reservation_data.get("pickupTime", ""),
                        "returnDate": reservation_data.get("returnDate", ""),
                        "returnTime": reservation_data.get("returnTime", ""),
                    })

            return matching_reservations

        except Exception as e:
            print(Strings.ERROR_FIREBASE_GET_CURRENT_RESERVATION.format(e))
            raise e

